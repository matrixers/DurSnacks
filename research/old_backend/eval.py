"""
Evaluation. Problem versus surface.

    python -m Backend.eval [--method raw,profile,blend] [--label step1] [--review]

Test A  one problem written in three centuries' styles: siblings should be nearest neighbours.
Test B  one topic, three different problems: nearest neighbour should share the PROBLEM, not the TOPIC.
Test C  one feeling and situation, three different stated CAUSES; the same cause types recur
        across groups: nearest neighbour should share the CAUSE, not only the feeling+situation.
pairs.json (optional, from historians): {"query", "passage_contains"}; share found in the top 5.

All test sentences are self-written and few (Test A 33, B 18, C 24): one sentence moves a
score by 0.03-0.06. Sentences marked NEW were added before any tuning (Step 1).
--review writes a blind side-by-side sheet of top passages per method for a person to judge.
"""
import datetime
import json
import os
import random
import sys

import numpy as np

from Backend import cards
from Backend.Backend import DEMO, METHODS, find, library

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_MD = os.path.join(ROOT, "RESULTS.md")
PAIRS = os.path.join(ROOT, "Backend", "pairs.json")

SAME_PROBLEM = {
    "abandonment": [
        "He has left me on read for a week and I keep checking my phone.",
        "Three weeks have passed and still no letter comes from her; I watch for the post each morning.",
        "No messenger has come from you since the Ides, and I wait at the gate each evening."],
    "failure": [
        "I failed my exams and everyone on my course did better than me.",
        "My book has been received with contempt, and I fear I have no talent whatever.",
        "My speech before the Senate was laughed at, and I am ashamed to show my face in the forum."],
    "grief": [
        "My dad died in March and I still pick up my phone to call him.",
        "Since my brother was buried I cannot enter his room without weeping.",
        "I have lost my daughter, and the house is silent where her voice used to be."],
    "homesickness": [
        "I moved abroad for uni and I miss my mum's cooking and my own bed.",
        "I am a stranger in this great city and think every hour of our village and my mother's fireside.",
        "Posted to this distant province, I long for Rome and the faces of my family."],
    "purpose": [
        "I have a good job but I do not see the point of any of it.",
        "I rise and work and sleep, and I cannot tell to what end I do it.",
        "I have held every office, yet I ask myself what all this labour has been for."],
    "money": [
        "My rent has gone up again and I am already in my overdraft.",
        "The creditors call daily and I have not a shilling to give them.",
        "I owe more than my estate is worth and the lenders press me hard."],
    "mortality": [
        "The doctor wants more tests and I am scared it is something serious.",
        "The physician shakes his head, and I fear I shall not see another spring.",
        "The fever returns each night and I think my end is near."],
    "envy": [
        "Everyone I know is getting promoted or engaged and I am stuck where I was.",
        "My schoolfellows are all risen in the world while I remain a poor clerk.",
        "Men younger than I are made consul while I am passed over year after year."],
    # NEW (Step 1, before tuning)
    "guilt": [
        "I shouted at my mum the night before she went into hospital and I can't take it back.",
        "I spoke harshly to my mother on the eve of her illness, and the words reproach me day and night.",
        "I spoke against my friend in the Senate, and now he is exiled and I cannot recall my words."],
    "heartbreak": [
        "She broke up with me over text and I can't stop looking at her photos.",
        "She has returned my letters unopened, and I cannot keep her face from my thoughts.",
        "Lesbia has turned from me to another, and still I burn for her."],
    "loneliness": [
        "I eat lunch alone every day and nobody at work talks to me.",
        "In all this crowded town there is not one soul to whom I can open my heart.",
        "In this great city I have no friend at my table and no one to speak with in the evenings."],
}

SAME_TOPIC = {
    "exams": {"failure": "I failed my exam and I feel stupid and worthless.",
              "abandonment": "My friend stopped answering me after the exam and I do not know why.",
              "purpose": "I passed the exam but I do not see what any of this study is for."},
    "work": {"failure": "My boss said my work is not good enough and I am ashamed.",
             "abandonment": "My colleague who was my friend left the job without a word to me.",
             "purpose": "My job pays well but the work feels empty and pointless."},
    "family": {"failure": "My family think I am a disappointment and I believe they are right.",
               "abandonment": "My sister no longer replies to me and I wait to hear from her.",
               "purpose": "I look after my family every day and wonder what my own life is for."},
    "moving": {"failure": "I moved to the city to succeed and I have achieved nothing.",
               "abandonment": "Since I moved away the person I love has gone silent.",
               "purpose": "I moved here for a fresh start and now nothing seems to matter."},
    # NEW (Step 1, before tuning)
    "friends": {"failure": "I let my team down in the final and I feel useless.",
                "abandonment": "My best friend stopped inviting me anywhere and won't say why.",
                "purpose": "I go out with my friends every weekend but it all feels empty."},
    "health": {"failure": "My injury stopped me finishing the race and I feel weak and pathetic.",
               "abandonment": "Since I got ill my friends have stopped visiting me.",
               "purpose": "I got better after my illness but I can't see what the point of recovering was."},
}

# NEW (Step 1). Cause types: R = others reject me, S = my own fault, C = circumstances outside my control.
SAME_FEELING_DIFFERENT_CAUSE = {
    "lonely in a new city": {
        "R": "I feel lonely in my new city because the people here don't want me around.",
        "S": "I feel lonely in my new city because I've been too shy to talk to anyone.",
        "C": "I feel lonely in my new city because I work night shifts and never get to meet anyone."},
    "anxious about exams": {
        "R": "I'm anxious about my exams because my parents will be cold to me if I fail.",
        "S": "I'm anxious about my exams because I wasted the whole term and didn't revise.",
        "C": "I'm anxious about my exams because they changed the syllabus at the last minute."},
    "sad a friendship ended": {
        "R": "I'm sad my friendship ended because she chose other people over me.",
        "S": "I'm sad my friendship ended because I said something cruel and pushed her away.",
        "C": "I'm sad my friendship ended because she had to move to Australia for her dad's job."},
    "angry at work": {
        "R": "I'm angry I was passed over at work because my boss has never liked me.",
        "S": "I'm angry I was passed over at work because I missed the deadline that mattered.",
        "C": "I'm angry I was passed over at work because the company froze all promotions this year."},
    "ashamed with family": {
        "R": "I feel ashamed around my family because they see me as a disappointment.",
        "S": "I feel ashamed around my family because I lied to them about dropping out.",
        "C": "I feel ashamed around my family because we lost the house when dad lost his job."},
    "heartbroken": {
        "R": "I'm heartbroken because he fell for someone else.",
        "S": "I'm heartbroken because I was jealous and controlling and drove him away.",
        "C": "I'm heartbroken because we had to split up when I was sent abroad for work."},
    "worried about money": {
        "R": "I'm worried about money because my family refuse to help me any more.",
        "S": "I'm worried about money because I spent my savings on stupid things.",
        "C": "I'm worried about money because my landlord raised the rent again."},
    "hopeless about the future": {
        "R": "I feel hopeless about my future because nobody will ever give me a chance.",
        "S": "I feel hopeless about my future because I gave up on my training years ago.",
        "C": "I feel hopeless about my future because my whole trade is disappearing."},
}

# Extra cases for the blind review sheet (wheel path + diary answers), beyond the 5 demo cases.
REVIEW_EXTRA = [
    (("Drained", "regretful"),
     {"event": "I said something cruel to my brother and now he won't speak to me.",
      "cause": "I lost my temper", "meaning": "that I have ruined the relationship for good"}),
    (("On edge", "anxious"),
     {"event": "My rent has gone up again and I am already in my overdraft.",
      "cause": "I cannot see how I will pay", "meaning": "that I will lose my home"}),
    (("On edge", "unsure what's next"),
     {"event": "The doctor wants more tests.", "cause": "it might be something serious",
      "meaning": "that I might not have much time"}),
    (("Small", "not good enough"),
     {"event": "Everyone I know is getting promoted or engaged.", "cause": "I am stuck where I was",
      "meaning": "that I am falling behind for good"}),
    (("Wound up", "rejected"),
     {"event": "My best friend moved to another city and stopped answering my messages.",
      "cause": "I think I did something wrong", "meaning": "that I am easy to leave"}),
]


def _reps(eng, texts):
    raw, prof = eng.embed(texts)
    return raw, prof


def _sim(raw, prof, w):
    s = w * (prof @ prof.T) + (1 - w) * (raw @ raw.T)
    np.fill_diagonal(s, -9)
    return s


def test_a(eng, methods):
    texts, labels = [], []
    for prob, variants in SAME_PROBLEM.items():
        texts += variants
        labels += [prob] * len(variants)
    labels = np.array(labels)
    raw, prof = _reps(eng, texts)
    out = {}
    for m in methods:
        top2 = np.argsort(_sim(raw, prof, METHODS[m]), axis=1)[:, ::-1][:, :2]
        out[m] = float(np.mean(labels[top2] == labels[:, None]))
    return out, 2 / (len(texts) - 1), len(texts)


def _nn_share(eng, groups, methods):
    texts, keys, grps = [], [], []
    for g, d in groups.items():
        for key, t in d.items():
            texts.append(t), keys.append(key), grps.append(g)
    keys, grps = np.array(keys), np.array(grps)
    raw, prof = _reps(eng, texts)
    out = {}
    for m in methods:
        nn = _sim(raw, prof, METHODS[m]).argmax(1)
        out[m] = (float(np.mean(keys[nn] == keys)), float(np.mean(grps[nn] == grps)))
    return out, len(texts)


def test_pairs(methods):
    if not os.path.exists(PAIRS):
        return None
    pairs = json.load(open(PAIRS, encoding="utf-8"))
    out = {}
    for m in methods:
        hits = 0
        for p in pairs:
            res = find(["?"], card=cards.Card(event=p["query"]).to_dict(), k=5, method=m)["results"]
            hits += any(p["passage_contains"] in r["text"] for r in res)
        out[m] = hits / len(pairs)
    return out, len(pairs)


def review_sheet(methods, label):
    """Blind sheet: for each case, the distinct top passages from all methods, shuffled."""
    rng = random.Random(0)
    lines, key = [f"# Blind review sheet ({label})", "",
                  "For each case, mark which passage(s) show someone facing the SAME underlying problem.",
                  "Methods are hidden; the key is in the matching *_key.json file.", ""], {}
    for n, (path, answers) in enumerate(DEMO + REVIEW_EXTRA, 1):
        tops = {m: find(path, answers, k=1, method=m)["results"][0] for m in methods}
        distinct = {}
        for m, r in tops.items():
            distinct.setdefault(r["passage_id"], (r, []))[1].append(m)
        items = list(distinct.values())
        rng.shuffle(items)
        lines += [f"## Case {n}: {' > '.join(path)}", "",
                  f"- what happened: {answers['event']}", f"- because: {answers['cause']}",
                  f"- afraid it means: {answers['meaning']}", ""]
        for j, (r, ms) in enumerate(items, 1):
            lines += [f"**{n}.{j}** {r['author']}, *{r['title']}* ({r['when']})", "",
                      f"> {r['text']}", "", "fits the problem? [ ] yes  [ ] partly  [ ] no", ""]
            key[f"{n}.{j}"] = ms
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    base = os.path.join(ROOT, "results", f"review_{label}")
    open(base + ".md", "w", encoding="utf-8").write("\n".join(lines))
    json.dump(key, open(base + "_key.json", "w", encoding="utf-8"), indent=1)
    return base + ".md"


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    methods = (argv[argv.index("--method") + 1].split(",") if "--method" in argv else list(METHODS))
    label = argv[argv.index("--label") + 1] if "--label" in argv else "run"
    lib = library()
    eng = lib.engine
    a, chance_a, n_a = test_a(eng, methods)
    b, n_b = _nn_share(eng, SAME_TOPIC, methods)
    c, n_c = _nn_share(eng, SAME_FEELING_DIFFERENT_CAUSE, methods)
    pairs = test_pairs(methods)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    head = (f"### {label} ({stamp}) - library {len(lib.rows)} passages, embedder {lib.emb.name}\n\n"
            f"| method | Test A same problem, top-2 (chance {chance_a:.2f}, n={n_a}) "
            f"| Test B NN problem / topic only (n={n_b}) "
            f"| Test C NN cause / feeling+situation only (chance {7/23:.2f} / {2/23:.2f}, n={n_c}) "
            f"| pairs.json top-5 |\n|---|---|---|---|---|")
    rows = []
    for m in methods:
        p = f"{pairs[0][m]:.2f} (n={pairs[1]})" if pairs else "missing"
        rows.append(f"| {m} (w={METHODS[m]}) | {a[m]:.2f} | {b[m][0]:.2f} / {b[m][1]:.2f} "
                    f"| {c[m][0]:.2f} / {c[m][1]:.2f} | {p} |")
    table = head + "\n" + "\n".join(rows) + "\n"
    print(table)
    if not pairs:
        print("pairs.json is missing (Backend/pairs.json): no historian query->passage pairs yet.")
    with open(RESULTS_MD, "a", encoding="utf-8") as f:
        if f.tell() == 0:
            f.write("# Results\n\nAppended by `python -m Backend.eval`. Newest at the bottom.\n\n")
        f.write(table + "\n")
    if "--review" in argv:
        print("review sheet:", review_sheet(methods, label))


if __name__ == "__main__":
    main(sys.argv)
