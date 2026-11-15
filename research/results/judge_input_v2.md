# Judge input (v2)

You are matching a person's problem to passages from real historical letters and diaries.

Goal: find a passage where the WRITER is facing the same underlying problem as the person:
the same emotion, the same kind of situation, felt for the same kind of reason, with the same fear.
A passage is more useful when it also shows how the writer deals with it: still struggling but
coping (writing to someone, keeping going, finding a way to see it) helps a reader more than pure
despair or an effortless triumph.
Sharing a topic or words is NOT enough (a passage about letters is not a match for "nobody replies to me"
unless the writer is the one waiting and hurt). A writer describing someone else's problem, giving advice,
or saying they are NOT troubled is not a match.

Judge only from the text given. Do not guess what the writer felt if the text does not show it.
"none" is a correct answer when no passage is a real match.

For each candidate give:
  emotion:   yes | partly | no      (the writer feels the same emotion)
  situation: yes | partly | no      (same kind of thing happening to the writer)
  cause:     yes | partly | no | not stated   (same kind of reason for the feeling)
  fear:      yes | partly | no | not stated   (same fear about what it means)
  coping:    none | despair | struggling | coping | resolved   (how the writer is dealing with it)
  overall:   yes | partly | no      (yes needs emotion and situation yes, and cause or fear yes/partly)
  why:       one short sentence, including how the writer deals with it if shown
Then give "best": the number of the single best candidate whose overall is yes or partly (when two
are equally close, prefer the one whose writer is struggling but coping), or "none".
Reply with JSON only, in exactly this format:

```json
{
 "verdicts": [
  {
   "n": 1,
   "emotion": "yes",
   "situation": "yes",
   "cause": "partly",
   "fear": "not stated",
   "coping": "struggling",
   "overall": "partly",
   "why": "..."
  }
 ],
 "best": 1
}
```

## Case 1: Heavy > lonely

```
(their own words)
  feeling (picked on a feelings wheel): lonely (heavy)
  what's happened: Nobody has replied to my messages in weeks.
  why they think they feel it: my friends seem to have forgotten me
  afraid: that I am easy to forget
  coping so far: I keep checking my phone

CANDIDATE PASSAGES
[1] George Jacob Holyoake, The History of the Last Trial by Jury for Atheism in England A Fragment of Autobiography Submitted for the Perusal of Her Majesty's Attorney-General and the British Clergy (1817–1906)
  context before: I answered, 'I think you have mistaken me. The opinions I defended are also my convictions; and thinking them useful, it seems my duty to propagate them, and the discharge of this duty is more serious in my eyes than you suppose; nor do the inducements you picture exist.
  PASSAGE: Do you not see that I am nearly friendless? I am without even the attentions of those from whom I have some right to expect it.
  context after: Except Mr. Farn, Mr. Watts, and Mr. Campbell, none of my colleagues among the Social Missionaries have written me a friendly word. The editor of the New Moral World, upon whose protection I have some claim, has written no word in my favour.

[2] Charles Lamb and Mary Lamb, The Works of Charles and Mary Lamb — Volume 5 The Letters of Charles and Mary Lamb, 1796-1820 (1775–1834)
  context before: We are necessarily confined with him the afternoon and evening till very late, so that I am stealing a few minutes to write to you. Thank you for your frequent letters, you are the only correspondent and I might add the only friend I have in the world.
  PASSAGE: I go no where and have no acquaintance. Slow of speech, and reserved of manners, no one seeks or cares for my society and I am left alone.
  context after: Allen calls only occasionally, as tho' it were a duty rather, and seldom stays ten minutes. Then judge how thankful I am for your letters.

[3] Jane Austen, The Letters of Jane Austen Selected from the compilation of her great nephew, Edward, Lord Bradbourne (1775–1817)
  context before: So you have C. Craven among you, as well as the Duke of Orleans and Mr. Pocock. But it mortifies me that you have not added one to the stock of common acquaintance.
  PASSAGE: Do pray meet with somebody belonging to yourself. I am quite weary of your knowing nobody.
  context after: Mrs. Digweed parts with both Hannah and old cook: the former will not give up her lover, who is a man of bad character; the latter is guilty only of being unequal to anything.
Miss Terry was to have spent this week with her sister, but as usual it is put off.

[4] Forbes Robinson, Letters to His Friends (1867–1904)
  context before: I am not that sort. I owe too much to you in the past ever to forget you. {133} I don't think that you really suspected me of inconstancy.
  PASSAGE: I am so sorry that you are sometimes lonely and very miserable. I feel at times weak, physically weak.
  context after: I think that at such times one can lean back, as it were, on the Divine arms. He understands our weakness and weariness.

[5] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 1 (1813–1883), translated by Francis Hueffer
  context before: -
  PASSAGE: Have you all forgotten me? I have felt so lonely of late that I am often afraid.
  context after: Should you be angry with me about anything? perhaps about the absurd misunderstanding with B.? He wrote to me that he had heard that I was annoyed at his great article on "Lohengrin."

[6] Karl May, My Life and My Efforts (1842–1912), translated by Gunther Olesch
  context before: And she wished with all of her heart that everything should turn out the way I yearned for it to be. And when she saw how firmly and unwaveringly I believed in my future, she believed as well and was as glad as a mother can be whose child is still thus fortunate, to be able to rely on God, mankind and himself.
  PASSAGE: But I felt lonely, lonely as always; because even in the entire town, there was not a single person who would have been willing or even able to understand me.
  context after: And for me, for me in particular, being thus harshly besieged in my inner self, this loneliness was dangerous in the highest degree. There was nothing I needed more than the company of someone who would understand me.

[7] Barbellion, W. N. P. and A. J. Cummings, A last diary (1889–1919)
  context before: February 3rd, 1919.--Suffering does not only insulate. It drops its victim on an island in an ocean desert where he sees men as distant ships passing.
  PASSAGE: I not only feel alone, but very far away from you all. But what is my suffering?
  context after: Not physical pain. I have none.

[8] Ralph Werther, Autobiography of an Androgyne (1874–?)
  context before: Proceeding in that direction, I stopped occasionally to make the same inquiry of other adolescents. After walking several blocks in vain, I returned to the “gang” at the warehouse’s portal, and asked: “Do you mind if I sit down to rest here?
  PASSAGE: I am tired and lonesome. I have not been in the city long and don’t know any one.”
  context after: “Where did yez come from?”
“Philadelphia.

[9] Cécile Tormay and Northumberland, Alan Ian Percy, An outlaw's diary: revolution (1876–1937)
  context before: That does not mend matters. A subdued moan resounds through the room, a pitiable, miserable little sound which comes from my heart....
  PASSAGE: Do others suffer as much as I do? I have spoken to nobody, have seen nobody.
  context after: I don’t know what they think. I have no one with whom to share my pain.

[10] Nina H. Kennard, Lafcadio Hearn (1844–1926)
  context before: My scholars in this great Government school are not boys, but men. They speak to me only in class.
  PASSAGE: The teachers never speak to me at all. I go to the college and return after class,--always alone, no mental company but books.
  context after: But at home everything is sweet."
In consequence of this isolation, or because of the softening influence of matrimony, here at Kumamoto he seemed for the first time to awake to the fact of having relations in that distant western land he had left so many years before.

[11] Arthur Christopher Benson, The Upton Letters (1862–1925)
  context before: Some nearness of life, some children of my own. You are apt to think of yourself as shelved and isolated; yet, after all, you have the real thing--wife, children, and home.
  PASSAGE: But, in my case, these boys who are dear to me have forgotten me already.
  context after: Disguise it as I will, I am part of the sordid furniture of life that they have so gladly left behind, the crowded corridor, the bare-walled schoolroom, the ink-stained desk. They are glad to think that they have not to assemble to-morrow to listen to my prosing, to bear the blows of the uncle's tongue, as Horace says.

[12] Honoré de Balzac, Letters to Madame Hanska, born Countess Rzewuska, afterwards Madame Honoré de Balzac, 1833-1846 (1799–1850), translated by Katharine Prescott Wormeley
  context before: I spare you the details of the agreement, which has been the object of long examination by my lawyers, and business agents, very devoted men, who think it good and honourable.
You could never believe how I miss the bulletin of your calm and solitary life, what interest I take in that life, and what peace the contemplation of it sheds upon my agitated life.
  PASSAGE: Either it is very bad of you to cut me off, or you are ill; on each side anxiety, thinking that you suffer or that your friendship diminishes.
  context after: Well, adieu. I meant to write you only one word: there is truce between misfortune and me.

[13] Andrew Everett Durham, Epistles from Pap: Letters from the man known as 'The Will Rogers of Indiana' (1882–1954)
  context before: I still bleed at the nose. . .My mental anguish is unbearable. I know that which I had in abundance and have ample living proof of is gone from me, never to return.
  PASSAGE: I have lost my social standing in the community in which I reside and my wimmen folks are laughing at me and at this time of the year. . .
  context after: Oh, grave, where is thy sting. . .
If you care to apologize for your hasty remarks about bull mental pain and anguish, you may address me as: Respectfully, The Bull

[14] Charles Lamb, The Best Letters of Charles Lamb (1775–1834)
  context before: I have offered my resignation, and it is neither accepted nor rejected. Eight weeks am I kept in this fearful suspense.
  PASSAGE: Guess what an absorbing stake I feel it. I am not conscious of the existence of friends present or absent.
  context after: The East India Directors alone can be that thing to me or not. I have just learned that nothing will be decided this week.

[15] Leo Tolstoy, The Journal of Leo Tolstoi (First Volume—1895-1899) (1828–1910), translated by Rose Strunsky
  context before: -
  PASSAGE: I feel that I am alone--that my life not only does not interest any one, but that they are bored and ashamed that I continue to occupy myself with such trifles.
  context after: I thought during this time:
1) A type of woman--there are men such also, but mostly it is women who are incapable of seeing themselves, as if their necks were stationary and they could not look back at themselves.

[16] John Muir, Letters to a Friend, Written to Mrs. Ezra S. Carr, 1866-1879 (1838–1914)
  context before: Yosemite, May 17th, 1870.
Our valley is just gushing, throbbing full of open, absorbable beauty, and I feel that I must tell you about it.
  PASSAGE: I am lonely among my enjoyments; the valley is full of visitors, but I have no one to talk to.
  context after: The season that is with us now is about what corresponds to full-fledged spring in Wisconsin. The oaks are in full leaf and have shoots long enough to bend over and move in the wind.

[17] Margaret Sanger, Margaret Sanger: an autobiography. (1879–1966)
  context before: Ethel handed it to me with the resigned comment, “Well, here’s your check from God.”
The editor of the Woman Rebel had struck her single match of defiance, but she could be of slight significance in the forward march towards “women’s rights.” In Feminist circles I was little known.
  PASSAGE: With my personal sorrow, my manifold domestic duties, my social shyness, I avoided meeting new people.
  context after: My attitude thus created some reluctance among those who might otherwise have hastened to my aid. Indeed, I wanted a certain type of support, but I could not take the initiative in asking for it.

[18] Humphry Ward, A Writer's Recollections — Volume 1 (1851–1920)
  context before: I have no courage for a letter to-day. I have just heard of the horrors of Paris, the burning of the Louvre, the Tuileries, the Hotel de Ville, etc.
  PASSAGE: My heart is wrung. I have energy for nothing. I cannot go out and see people.
  context after: I was in the Bodleian when the Librarian told me this and showed me the newspapers. In presence of such madness and such disasters, they treat a Frenchman here with a kind of pitying sympathy.

[19] Catherine Helen Spence, An Autobiography (1825–1910)
  context before: Will no one tell me what it means? I want to find the old unhappy far off things which Wordsworth imagined in the Gaelic song of the 'Highland Lass.'
  PASSAGE: I feel out of it, uneasy, thinking all the time what a poor creature I must be.
  context after: I remember the mother of the sonata players approaching me with beaming countenance on the occasion of one of these performances, expecting the compliment which I faltered forth, doing my best not to look insincere. 'And I have this every evening of my life,' cried the triumphant mother.

[20] Barbellion, W. N. P. and H. G. Wells, The journal of a disappointed man (1889–1919)
  context before: I could, if I would, surrender myself. Her affection makes me long to do it.
  PASSAGE: I am sick of living by myself. I am frightened of myself. My life is miserable alone, and sometimes desperately miserable when I long for a little sympathy to be close at hand.
  context after: I have often tried to persuade R---- to share a flat with me, because I don't really wish to marry. I struggle against the idea, I am egotist enough to wish to shirk the responsibilities.
```

## Case 2: Small > like a failure

```
(their own words)
  feeling (picked on a feelings wheel): like a failure (small)
  what's happened: I failed my exams and everyone on my course did better than me.
  why they think they feel it: I am not clever enough for this course
  afraid: that I will never make anything of myself
  coping so far: I have stopped going to lectures

CANDIDATE PASSAGES
[1] Andrew Dickson White, Autobiography of Andrew Dickson White — Volume 2 (1832–1918)
  context before: On my endeavoring to retain him, he answered as follows: "I have been over twelve years in the American diplomatic service as secretary; I have seen the secretaries here, from all other countries, steadily promoted until all of them still remaining in the service are in higher posts, several of them ministers, and some ambassadors. I remain as I was at the beginning, with no promotion, and no probability of any.
  PASSAGE: I feel that, as a rule, my present colleagues, as well as most officials with whom I have to do, seeing that I have not been advanced, look upon me as a failure.
  context after: They cannot be made to understand how a man who has served so long as secretary has been denied promotion for any reason save inefficiency. I can no longer submit to be thus looked down upon, and I must resign."

[2] Marcus Tullius Cicero, Cicero: Letters to Atticus, Vol. 2 of 3 (107 BC–44 BC), translated by Eric Otto Winstedt
  context before: Antony says he has received orders about me definitely. Yet I have not seen him myself so far; but he told Trebatius.
  PASSAGE: What can I do now? Nothing succeeds and all my best laid plans fail abominably.
  context after: For, when I had won over Curio, I imagined I had attained my end. He had written about me to Hortensius.

[3] Henri Frédéric Amiel, Amiel's Journal: The Journal Intime of Henri-Frédéric Amiel (1821–1881), translated by Mrs. Humphry Ward
  context before: I took account of my faults, and they ranged themselves in battle against me. The vulture of regret gnawed at my heart, and the sense of the irreparable choked me like the iron collar of the pillory.
  PASSAGE: It seemed to me that I had failed in the task of life, and that now life was failing me.
  context after: Ah! how terrible spring is to the lonely! All the needs which had been lulled to sleep start into life again, all the sorrows which had disappeared are reborn, and the old man which had been gagged and conquered rises once more and makes his groans heard.

[4] Anthony Trollope, An Autobiography of Anthony Trollope (1815–1882)
  context before: I do not think that the failure--for it did fail--arose from bad editing. Perhaps too much editing might have been the fault.
  PASSAGE: I was too anxious to be good, and did not enough think of what might be lucrative.
  context after: It did fail, for it never paid its way. It reached, if I remember right, a circulation of nearly 10,000--perhaps on one or two occasions may have gone beyond that.

[5] Robert Louis Stevenson, The Letters of Robert Louis Stevenson — Volume 2 (1850–1894)
  context before: I am myself very ready; or would be—will be—when I have made a little money for my folks. The blows that have fallen upon you are truly terrifying; I wish you strength to bear them.
  PASSAGE: It is strange, I must seem to you to blaze in a Birmingham prosperity and happiness; and to myself I seem a failure.
  context after: The truth is, I have never got over the last influenza yet, and am miserably out of heart and out of kilter. Lungs pretty right, stomach nowhere, spirits a good deal overshadowed; but we’ll come through it yet, and cock our bonnets.

[6] Madame de Maintenon and of Savoy Marie Adelaide, The Correspondence of Madame, Princess Palatine, Mother of the Regent; of Marie-Adélaïde de Savoie, Duchesse de Bourgogne; and of Madame de Maintenon, in Relation to Saint-Cyr (1635–1719)
  context before: Submit, if you wish to remain; but, if you wish to leave, it will be more honourable to you to do so by agreement with me than to get yourself dismissed. You are lax and cold towards God; it is that which makes you fall into all these faults.
  PASSAGE: Reflect, I beg of you, on what you might hope of yourself on the occasions which you will find to fail.
  context after: You are becoming grown-up; this is the time to make serious reflections. It is for God, my dear child, to touch your heart, but it is for us to rule your conduct.

[7] Henry James, The Letters of Henry James (Vol. I) (1843–1916)
  context before: I don't think you go far enough, and you are haunted with romantic phantoms and a tendency to factitious glosses; but you are in the right path, and I wish you repeated triumphs there--beginning with your Americo-Venetian--though I slightly fear, from what you tell me, that he will have a certain "gloss." It isn't for me to reproach you with that, however, the said gloss being a constant defect of my characters; they have too much of it--too damnably much.
  PASSAGE: But I am a failure!--comparatively. Read Zola's last thing: La Joie de Vivre. This title of course has a desperate irony: but the work is admirably solid and serious....
  context after: Addio--stia bene. I wish you could send me anything you have in the way of advance-sheets.

[8] Anton Chekhov, Letters to His Family and Friends (1890), translated by Constance Garnett
  context before: It is all the same to me whether I write “The Party” or “The Lights,” or a vaudeville or a letter to a friend--it is all dull, spiritless, mechanical, and I get annoyed with critics who attach any importance to “The Lights,” for instance. I fancy that I deceive him with my work just as I deceive many people with my face, which looks serious or over-cheerful.
  PASSAGE: I don’t like being successful; the subjects which sit in my head are annoyed and jealous of what has already been written.
  context after: I am vexed that the rubbish has been done and the good things lie about in the lumber-room like old books. Of course, in thus lamenting I rather exaggerate, and much of what I say is only my fancy, but there is a part of the truth in it, a good big part of it.

[9] Goethe, Johann Wolfgang von, The Autobiography of Goethe Truth and Poetry: From My Own Life (1749–1832), translated by A. J. W. Morrison
  context before: Now as I likewise saw the advantages of it in society, I easily suffered myself to be led by her. I had indeed the sense of play, but not the spirit of play; I learned all games easily and rapidly, but I could never keep up the proper attention for a whole evening.
  PASSAGE: Therefore, when I began very well, I invariably failed at the end, and made myself and others lose; through which I went off, always out of humour, either to the supper-table or out of the company.
  context after: Scarcely was Madame Böhme dead, who, moreover, had no longer kept me in practice during her tedious illness, than my father's doctrine gained force; I at first excused myself from the card-tables, and as they now did not know what else to do with me, I became even more of a burden to myself than to others, and declined the imitations, which then became more rare, and at last ceased altogether. Play, which is much to be recommended to young people, especially to those who have a practical sense, and wish to look about in the world for themselves, could never, indeed, become a passion with me; for I never got further, though I might play as long as I would.

[10] Mark Twain, Mark Twain's Letters — Volume 2 (1867-1875) (1835–1910)
  context before: I wish I had gone to Washington in the winter instead of going West. I could have gouged an office out of Bill Stewart for him, and that would atone for the loss of my home visit.
  PASSAGE: But I am so worthless that it seems to me I never do anything or accomplish anything that lingers in my mind as a pleasant memory.
  context after: My mind is stored full of unworthy conduct toward Orion and towards you all, and an accusing conscience gives me peace only in excitement and restless moving from place to place. If I could say I had done one thing for any of you that entitled me to your good opinion, (I say nothing of your love, for I am sure of that, no matter how unworthy of it I may make myself, from Orion down you have always given me that, all the days of my life, when God Almighty knows I seldom deserve it,) I believe I could go home and stay there and I know I would care little for the world's praise or blame.

[11] Louis Spohr, Louis Spohr's Autobiography Translated from the German (1784–1859)
  context before: With every successive rehearsal these were made more clear to me, and even before its production in public took place, the Opera (with the exception of the Overture and one aria for a tenor-voice) had become distasteful to me. Even the great applause it had met with from those who executed it, and those who heard it, could not reconcile me the more to it; so that I laid it aside, and with the exception of the two “Numbers” mentioned, I never played any thing more of it in public.
  PASSAGE: But with this feeling of dissatisfaction with my work I was truly unhappy; for I now thought to perceive that I had no talent for Operatic compositions.
  context after: There were, however, two things which I had forgotten duly to consider; first, that I had assumed a much too elevated style, for I had put my Opera upon a par with those of Mozart, and secondly, that I was wholly wanting in the practice and experience requisite for this kind of composition. This did not occur to me till some years afterwards, and encouraged me then to make another attempt at dramatic composition.

[12] Henry David Thoreau, Journal 01, 1837-1846 The Writings of Henry David Thoreau, Volume 07 (of 20) (1817–1862)
  context before: It is all a mystery to him. "How happens it," he exclaims, "that I find myself making such an enormous demand on men, and so constantly disappointed?
  PASSAGE: Are my friends aware how disappointed I am? Is it all my fault? Am I incapable of expansion and generosity?
  context after: I shall accuse myself of anything else sooner." And again he goes away sorrowful, consoling himself, as best he can, with his own paradox,—

[13] Sarah Morgan Dawson, A Confederate Girl's Diary (1842–1909)
  context before: Have I exerted fully the natural desire To Know that is implanted in all hearts? Have I done myself injustice in my self-taught ignorance, or has injustice been done to me?
  PASSAGE: Where is the fault, I cried. Have I labored to improve the few opportunities thrown in my path, to the best of my ability?
  context after: "Answer for yourself. With the exception of ten short months at school, where you learned nothing except arithmetic, you have been your own teacher, your own scholar, all your life, after you were taught by mother the elements of reading and writing.

[14] Walter Scott, The Journal of Sir Walter Scott From the Original Manuscript at Abbotsford (1771–1832)
  context before: Well, it would be my risk, and if I can do some good, which I rather think I can, is it right or manly to keep myself back?
Third.--I feel myself decidedly weaker in point of health, and am now confirmed I have had a paralytic touch.
  PASSAGE: I speak and read with embarrassment, and even my handwriting seems to stammer. This general failure
  context after: -

[15] Simon Newcomb, The Reminiscences of an Astronomer (1835–1909)
  context before: I felt its importance at the time. As I walked and walked, the question in my mind was, what am I doing and whither am I going?
  PASSAGE: Am I doing right or wrong? Am I going forward to success in life, or to failure and degradation?
  context after: Vainly, vainly, I tried to peer into the thick darkness of the future. No definite idea of what success might mean could find a place in my mind.

[16] Lafcadio Hearn, Letters from the Raven: Correspondence of L. Hearn with Henry Watkin (1850–1904)
  context before: No man could have helped doing anything already done. I hate the gilded slavery of newspaper work,--the starvation of Bohemianism,--the bore of waiting for a chance to become an insurance agent or a magazine writer,--and oh, venerable friend, I hate a thousand times worst of all to work for somebody else.
  PASSAGE: I hoped to become independent when I came down here,--to work for myself; and I have made a most damnable failure of it.
  context after: In addition to the rest, my horrid eye is bad yet. I had lost nearly half the field of vision from congestion of the retina when I wrote you the rather frantic epistles which you would not answer.

[17] Egerton Ryerson, "The story of my life" (1803–1882)
  context before: I cannot but see that the public mind in this country is in a chaotic state, without any controlling current of feeling, or fixed principle of action, in civil affairs; but susceptible, by proper management and instruction, of being cast into any mould of rational opinion and feeling; yet liable, without judicious direction, to fall into a state of "confusion worse confounded." I know that now is the time--perhaps the only time--to establish our institutions and relations upon the cheapest, the surest, and the only permanent foundation of any system, or form of Government--the sentiments and feelings of the population.
  PASSAGE: But I alone have not the means or the power of contributing to the accomplishment of these objects.
  context after: To the utmost of my humble abilities and acquirements, I am willing to exert myself; and that without a shillings' remuneration--although my present salary is less than L200 per annum. I believe the government about to be established in these provinces may be made the most enduring and loftiest memorial of your Excellency's fame, and the greatest earthly blessing to its inhabitants; and it will be to me a source of satisfaction to contribute towards the formation and cementing of materials for the erection of a monument at once so honourable to its founder, and so beneficial to Her Majesty's Canadian subjects.

[18] Charles Darwin, Life and Letters of Charles Darwin — Volume 2 (1809–1882)
  context before: Soc., but by Jove the Linn. Soc. produced a tremendous effect on me, for I could not get out of bed till late next evening, so that I just crawled home.
  PASSAGE: I fear I must give up trying to read any paper or speak; it is a horrid bore, I can do nothing like other people."
  context after: To Dr. Gray he wrote, (December 1861):--
"You may rely on it, I will send you a copy of my Primula paper as soon as I can get one; but I believe it will not be printed till April 1st, and therefore after my Orchid Book.

[19] Ida M. Tarbell, All in the Day's Work: An Autobiography (1857–1944)
  context before: I began to train my mind to go at its task regularly, keep hours, study whether I liked a thing or not. I forced myself not to waste time, not to loaf, not to give up before I finished.
  PASSAGE: If I failed at any point in this discipline I suffered a certain mental and spiritual malaise, a dissatisfaction with myself hard to live with.
  context after: In spite of my painful efforts to make a regular worker out of myself, life at college was lightened by my discovery of the Boy. Incredible as it seems to me now, I had come to college at eighteen without ever having dared to look fully into the face of any boy of my age.

[20] W. H. Davies and Bernard Shaw, The Autobiography of a Super-Tramp (1871–1940)
  context before: It was now the latter end of October, and this pound could not reach London far short of a month. Thinking I was not likely again to suffer for want of a bed or food, after this success in Swindon, I bought a good stock of laces and left that town, with the intention of working the towns on the outskirts of London, so that when ready to enter I would be within a day's march.
  PASSAGE: Unfortunately, after leaving Swindon, success deserted me, which was certainly more my fault than that of the people, for I made very little appeal to them.
  context after: Arriving at Maidenhead, I had the bare price of my bed, with a dry bread supper and breakfast. My laces were being exhausted, and I was without means to replenish them.
```

## Case 3: Heavy > grieving

```
(their own words)
  feeling (picked on a feelings wheel): grieving (heavy)
  what's happened: My dad died this year.
  why they think they feel it: I miss him and I do not know how to carry on without him
  afraid: that the best part of my life is over
  coping so far: I keep busy so I don't have to think

CANDIDATE PASSAGES
[1] William Jackson Elmslie, Seedtime in Kashmir: A Memoir of William Jackson Elmslie (1832–1872)
  context before: She replied, "Not a strong hope, but with a hope," and then she went on to quote several very appropriate promises out of the Word of God.
In due course the news of her death reached Dr. Elmslie, and, writing to his friend, Mr. Rodgers, he says (17th August 1869):–"You see, my dear Rodgers, that I am become one of the mourners.
  PASSAGE: My best and dearest friend on earth is dead–my mother. You can more easily picture to yourself my intense grief than I can describe it to you.
  context after: Since Sabbath last, I scarcely know what I have been about. I have been doing my work, but I have had no mind for it.

[2] Asa Gray, Letters of Asa Gray; Vol. 2 (1810–1888)
  context before: If still there I should go to see him; but he has now gone to Gries, in Appenzell, to a bathing-place, and I shall not see him.... Reuter, his curator, was away last week, but I shall see him, I presume, to-morrow.
  PASSAGE: I have just lost my mother, at a good old age. My father died twenty-four years earlier....
  context after: It is a charming place here. We are spending the morning lazily, and go on soon to Geneva.

[3] Helen Keller, The Story of My Life With her letters (1887-1901) and a supplementary account of her education, including passages from the reports and letters of her teacher, Anne Mansfield Sullivan, by John Albert Macy (1880–1968)
  context before: But, however this may be, I cannot now write the letter which has lain in my thought for you so long. My heart is too full of sadness to dwell upon the happiness the summer has brought me.
  PASSAGE: My father is dead. He died last Saturday at my home in Tuscumbia, and I was not there.
  context after: My own dear loving father! Oh, dear friend, how shall I ever bear it!...

[4] Robert Louis Stevenson, The Letters of Robert Louis Stevenson — Volume 1 (1850–1894)
  context before: But the man who loves art with wisdom sees the joke; it is the lustful that tremble and respect her ladyship; but the honest and romantic lovers of the Muse can see a joke and sit down to laugh with Apollo.
The prospect of your return to Europe is very agreeable; and I was pleased by what you said about your parents.
  PASSAGE: One of my oldest friends died recently, and this has given me new thoughts of death.
  context after: Up to now I had rather thought of him as a mere personal enemy of my own; but now that I see him hunting after my friends, he looks altogether darker. My own father is not well; and Henley, of whom you must have heard me speak, is in a questionable state of health.

[5] Marcus Tullius Cicero, Cicero: Letters to Atticus, Vol. 2 of 3 (107 BC–44 BC), translated by Eric Otto Winstedt
  context before: -
  PASSAGE: take this grief away from me, or at any rate lessen it by your sympathy or advice or by any other possible means.
  context after: Yet what can you or any man do? God Himself could hardly help now.

[6] Charles Lamb and Mary Lamb, The Works of Charles and Mary Lamb — Volume 6 Letters 1821-1842 (1775–1834)
  context before: My dear Wordsworth--A letter from you is very grateful, I have not seen a Kendal postmark so long! We are pretty well save colds and rheumatics, and a certain deadness to every thing, which I think I may date from poor John's Loss, and another accident or two at the same time, that has made me almost bury myself at Dalston, where yet I see more faces than I could wish.
  PASSAGE: Deaths over-set one and put one out long after the recent grief. Two or three have died within this last two twelvem'ths, and so many parts of me have been numbed.
  context after: One sees a picture, reads an anecdote, starts a casual fancy, and thinks to tell of it to this person in preference to every other--the person is gone whom it would have peculiarly suited. It won't do for another.

[7] John Adams and Abigail Adams, Familiar Letters of John Adams and His Wife Abigail Adams During the Revolution with a Memoir of Mrs. Adams (1735–1826)
  context before: Such an Eastern circuit I never made. I shall bring home as much as I brought from home, I hope, and not much more, I fear.
  PASSAGE: I go mourning in my heart all the day long, though I say nothing. I am melancholy for the public and anxious for my family.
  context after: As for myself, a frock and trousers, a hoe and a spade would do for my remaining days.
For God's sake make your children hardy, active, and industrious; for strength, activity and industry will be their only resource and dependence.

[8] Jonathan Swift, The Journal to Stella (1667–1745)
  context before: I thought to have sent this to-night, but was kept by company, and could not; and, to say the truth, I had a little mind to expect one post more for a letter from MD. Yesterday at noon died the Earl of Anglesea, {13c} the great support of the Tories; so that employment of Vice-Treasurer of Ireland is again vacant.
  PASSAGE: We were to have been great friends, and I could hardly have a loss that could grieve me more.
  context after: The Bishop of Durham {14a} died the same day. The Duke of Ormond’s daughter {14b} was to visit me to-day at a third place by way of advance, {14c} and I am to return it to-morrow.

[9] William Quan Judge and Keightley, Julia Wharton Lewis Campbell Ver Planck, Letters That Have Helped Me (1851–1896)
  context before: In order to off-set the terribly cold effect of perceiving the littleness of human affairs, one must inculcate in oneself a great compassion which will include oneself also. If this is not done, contempt comes on, and the result is dry, cold, hard, repellent and obstructive to all good work.
  PASSAGE: I know that his absence is a loss to you, but I think if you will regard all things and events as being in the Self and It in them, making yourself a part of the whole, you will see there is no real cause for sorrow or fear.
  context after: Try to realise this and thus go in confidence and even joy.
* * * * *

[10] Edward FitzGerald, Letters of Edward FitzGerald, in Two Volumes. Vol. 2 (1809–1883)
  context before: Of Tennyson I hear but little: and I have ceased to look forward to any future Work of his. Thackeray seems dumb as a gorged Blackbird too: all growing old!
  PASSAGE: I have lost my sister Kerrich, the only one of my family I much cared for, or who much cared for me.
  context after: But (not to dwell on what cannot be helped, and to which my talking of all growing old led me) I see in last week's Athenaeum great Praise of a new Volume of Poems by Jean Ingelow. The Reviewer talks of a 'new Poet,' etc., quite unaware that some dozen years ago the 'new Poet' published a Volume (as you may remember) with as distinct Indications of sweet, fresh, and original Genius as anything he adduces from this second Volume.

[11] Alfred Russel Wallace and James Marchant, Alfred Russel Wallace: Letters and Reminiscences, Vol. 2 (1823–1913)
  context before: Pray accept our sincere sympathy for Mrs. Marshall and yourself.
Death makes us feel, in a way nothing else can do, the mystery of the universe.
  PASSAGE: Last autumn I lost my sister, and she was the only relative I have been with at the last.
  context after: For the moment it seems unnatural and incredible that the living self with its special idiosyncrasies you have known so long can have left the body, still more unnatural that it should (as so many now believe) have utterly ceased to exist and become nothingness!
With all my belief in, and knowledge of, Spiritualism, I have, however, occasional qualms of doubt, the remnants of my original deeply ingrained scepticism; but my reason goes to support the psychical and spiritualistic phenomena in telling me that there must be a hereafter for us all....--Believe me yours very sincerely,

[12] Annie Besant, Autobiographical Sketches (1847–1933)
  context before: -
  PASSAGE: The two months after my mother's death were the dreariest my life has known, and they were months of tolerably hard struggle.
  context after: The little house in Colby Road taxed my slender resources heavily, and the search for work was not yet successful. I do not know how I should have managed but for the help, ever at hand, of Mr. and Mrs. Thomas Scott.

[13] William James Stillman, The Autobiography of a Journalist, Volume II (1828–1901)
  context before: To me Russie's death was a crushing disaster. The care and constant preoccupation of my life was taken away, and nothing moved me to activity.
  PASSAGE: I missed him every moment that I was awake, and in my condition I could not rally from the depression caused by the mental void and grief.
  context after: I do not think I should have recovered from it had not Mr. Spartali conceived the idea of my going off to Herzegovina, where the insurrection of 1875 was just beginning to stir, and, to cut short my hesitation at the venture as a volunteer correspondent, got me an introduction to the manager of the "Times," and offered to pay my expenses should the "Times" not accept my letters. I knew so well the condition in which the Turkish Empire had been left by the Cretan affair, and the apathy that had ruled ever since, that I was convinced that a disaster was pending, and the state to which Russia had brought matters in the Ottoman Empire in 1869 pointed to a Slavonic movement this time.

[14] Sarah Morgan Dawson, A Confederate Girl's Diary (1842–1909)
  context before: We can only die once; we can suffer a thousand deaths with suspense and uncertainty; the shortest is the best. Do you think the few words here can give an idea of our agony and despair?
  PASSAGE: Nothing can express it. I feel a thousand years old to-day. I have shed the bitterest tears to-day that I have shed since father died.
  context after: I can't stand it much longer; I'll give way presently, and I know my heart will break. Shame!

[15] Sévigné, Marie de Rabutin-Chantal, The letters of Madame de Sévigné (1626–1696)
  context before: -
  PASSAGE: It was yesterday three years that I felt the most poignant grief of my whole life.
  context after: You set out at that time for Provence, and you remain there still. My letter would be very long, if I attempted to express all the sorrow I then felt, and what I have since felt, in consequence of this separation.

[16] Peter Abelard and Héloïse, The love letters of Abelard and Heloise (1079–1142)
  context before: Can my feeble reason resist such powerful assaults? When I am distracted and raving (if I dare say it) even against Heaven itself, I shall not soften it by my cries, but rather provoke it by my reproaches.
  PASSAGE: How should I pray or how bear up against my grief? I should be more eager to follow you than to pay you the sad ceremonies of a funeral.
  context after: It is for you, for Abelard, that I have resolved to live, and if you are ravished from me I can make no use of my miserable days. Alas! what lamentations should I make if Heaven, by a cruel pity, preserved me for that moment?

[17] Edward Gibbon, Private Letters of Edward Gibbon (1753-1794) Volume 2 (of 2) (1737–1794)
  context before: When I had the pleasure of seeing you at Bath two years ago, you may remember the melancholy account which I gave you of poor Deyverdun. On my return to Lausanne I found him much altered for the worse; he was attacked by a succession of Apoplectic fits, and after a general decay, he died last July, when his life could be no longer desirable for himself or his friends.
  PASSAGE: The loss of a friend of five and thirty years is irreparable, and each day I feel the comfortless solitude to which I am reduced.
  context after: By his will he designed that I should possess the delightful house and garden which I inhabit: and which have not, I believe, their equal in Europe; by a subsequent arrangement with his heir, in which both find their advantage, I have secured the free and indisputable enjoyment for my life, and have already made some agreable and useful alterations. I still like the people and the country, and here I shall probably spend the latter season of life, with the resolution however of visiting England every three or four years.

[18] Benito Mussolini and Richard Washburn Child, My autobiography (1883–1945)
  context before: I was only twenty-nine years old when at Reggio Emilia at the Congress in 1912, two years before the World War began, I was nominated as director of the Avanti. It was the only daily of the socialist cause and was published in Milan.
  PASSAGE: I lost my father just before I left for my new office. He was only fifty-seven.
  context after: Nearly forty of those years had been spent in politics. His was a rectangular mind, a wise spirit, a generous heart.

[19] Sunity Devee, Maharani of Cooch Behar, The Autobiography of an Indian Princess (1864–1932)
  context before: His voice is hushed and no one will ever again look upon his dear face, but his soul lives on in the Land Immortal where he has been called to greater work. I am longing to be with my loved ones who have gone before, to be where we shall never part again.
  PASSAGE: This sad loss has brought a great change into my life. I feel the unknown world is very near to me and I must try and finish what I think I have to do quickly.
  context after: God gifted me with everything that was precious, and one thing I wish to leave behind me and that is Love. I feel my strength has gone and often wonder why I am left.

[20] Hare, Augustus J. C., The Story of My Life, volumes 4-6 (1834–1903)
  context before: In the six death-beds I have attended it has been so; and even in this case, when it lasted four days and nights, there was little speech, only an urgency that I should never leave her, that I should keep near her, that I should be close by her side as long as she was on earth at all, till she passed into the unseen.
“Whilst feeling the change which her loss makes in my life, I have read words of Bishop Magee which have come home to me. ‘The most beautiful and natural of sunsets is still a sunset, and the shadows that follow it are chill and depressing.
  PASSAGE: I begin to feel the peculiar sadness that the death of much older relatives brings to those who are entering themselves on old age.
  context after: When I see all those whom I remember once, middle-aged men and women, younger by many years than I am now, all passed and gone, I feel somehow as if light was going out of life very fast. There are so few living with whom one can recall the past, and grow young again in recalling it.’”
```

## Case 4: Heavy > homesick

```
(their own words)
  feeling (picked on a feelings wheel): homesick (heavy)
  what's happened: I moved to a new city for university.
  why they think they feel it: I miss home and my family so much
  afraid: that I do not belong here
  coping so far: I call my mum every night

CANDIDATE PASSAGES
[1] Elizabeth Barrett Browning, The Letters of Elizabeth Barrett Browning (Volume 2 of 2) (1806–1861)
  context before: We have done duty to the north too lately. Now it seems to me we have the right (of virtue, in spite of what I said on another page, or rather, because I said it in good human inconsistency), the right to have and hold our Italy in undisturbed possession.
  PASSAGE: I never feel at home anywhere else, or to live rightly anywhere else at all.
  context after: It's a horrible want of patriotism, of course, only, if I were upon trial, I might say in a low voice a few things to soften the judgment against me on account of that sin. Ah! we missed you at Havre!

[2] Lucie Duff Gordon, Letters from Egypt (1821–1869)
  context before: -
  PASSAGE: I am tolerably well, but I am growing very homesick--or rather children-sick. As the time slips on I get more and more the feeling of all I am losing of my children.
  context after: We have delicious weather here and have had all the time; there has been no cold at all this winter here.
M. Prevost Paradol is here for a few days--a very pleasant man indeed, and a little good European talk is a very agreeable interlude to the Arab prosiness, or rather enfantillage, on the part of the women.

[3] Margaret Sanger, Margaret Sanger: an autobiography. (1879–1966)
  context before: I was trying to prove the law was wrong, not I. Giving Mr. Pollock no directions how to act, I merely said I would call him up.
It was now four o’clock and I sought refuge at home to think through my mental turmoil and distress.
  PASSAGE: But home was crowded with too many associations and emotions pulling me this way and that.
  context after: When my thoughts would not come clear and straight I packed a suitcase, went back downtown, and took a room in a hotel, the most impersonal place in the world.
There was no doubt in my mind that if I faced the hostile court the next morning, unprepared as I was, I would be convicted of publishing an obscene paper.

[4] Charles Lever, Charles Lever, His Life in His Letters, Vol. II (1806–1872)
  context before: “Croce di Malta, Spezzia, Dec. 30, 1866.
“Your last pleasant note and its ‘stuffing’ has just reached me here, where I am consularising, bullying Custom-house folk, and playing the devil with all the authorities to show my activity in the public service.
  PASSAGE: I can’t endure being away from home and my old routine life; but there was no help for it, and I am here now for another week to come.
  context after: “The name I want for the author of Tony is ‘Arthur Helsham,’ the name of my mother’s family; and the last man who bore the aforesaid was the stupidest blockhead of the house, and the luckiest too. Faustum sit augurium.

[5] Maud Howe Elliott, Three generations (1854–1948)
  context before: -
  PASSAGE: I am growing to feel at home in this queer grimy city. Life is pretty laborious.
  context after: We get to the studio at nine. I drape J’s model, an old German soldier posing for St. Peter.

[6] Henry James, The Letters of Henry James (Vol. II) (1843–1916)
  context before: This address will find me till the end of June--but Lamb House of course always. I have taken three or four (or five) years' lease of a small flat on this pleasant old Chelsea riverside to hibernate in for the future.
  PASSAGE: I return to the country for five or six months of summer and autumn, but can't stand the utter solitude and confinement of it from December to the spring's end.
  context after: Ah, had we only a climate!--yours or Fanny Stevenson's (if she is still the exploiter of climates)--I believe I should be all right then! Tell me of her--and tell me of your Mother.

[7] Walter Scott, The Journal of Sir Walter Scott From the Original Manuscript at Abbotsford (1771–1832)
  context before: February 12.--Having ended the second volume of Woodstock last night, I have to begin the third this morning. Now I have not the slightest idea how the story is to be wound up to a catastrophe.
  PASSAGE: I am just in the same case as I used to be when I lost myself in former days in some country to which I was a stranger.
  context after: I always pushed for the pleasantest road, and either found or made it the nearest. It is the same in writing, I never could lay down a plan--or, having laid it down, I never could adhere to it; the action of composition always diluted some passages, and abridged or omitted others; and personages were rendered important or insignificant, not according to their agency in the original conception of the plan, but according to the success, or otherwise, with which I was able to bring them out.

[8] Sarah Morgan Dawson, A Confederate Girl's Diary (1842–1909)
  context before: But I take it all out in here. I believe I must be made of wood, or some other tough material, not to feel it more.
  PASSAGE: I sometimes ask myself if it is because I did not care for home, that I take it so quietly now.
  context after: But I know that is not it. I was wild about it before I knew what had happened; since I learned all, few are the words that have escaped my lips concerning it.

[9] Robert E. Lee, Recollections and Letters of General Robert E. Lee (1843–1914)
  context before: “Richmond, May 25, 1861.
“I have been trying, dearest Mary, ever since the receipt of your letter by Custis, to write to you.
  PASSAGE: I sympathise deeply in your feelings at leaving your dear home. I have experienced them myself, and they are constantly revived.
  context after: I fear we have not been grateful enough for the happiness there within our reach, and our Heavenly Father has found it necessary to deprive us of what He has given us. I acknowledge my ingratitude, my transgressions, and my unworthiness, and submit with resignation to what he thinks proper to inflict upon me.

[10] George Eliot, George Eliot's Life, as Related in Her Letters and Journals. Vol. 3 (of 3) (1819–1880)
  context before: Dr. Reynolds recommended the Yorkshire coast; but we wanted to know Cromer, and so we came here first, for the sake of variety. To me the most desirable thing just now seems to be to have one home, and stay there till death comes to take me away.
  PASSAGE: I get more and more disinclined to the perpetual makeshifts of a migratory life, and care more and more for the order and habitual objects of home.
  context after: However, there are many in the world whose whole existence is a makeshift, and perhaps the formula which would fit the largest number of lives is "a doing without, more or less patiently." The air just now is not very invigorating anywhere, I imagine, and one begins to be very anxious about the nation generally, on account of the threatening drought.

[11] Fanny Kemble, Records of Later Life (1809–1893)
  context before: I know that very unprincipled people are capable of affection, and their affection partakes of their want of principle: people have committed crimes for the sake of the love they bore their wives, mistresses (oftener), and children; and half the meannesses, pettinesses, and selfishnesses of which society is full, have their source in unprincipled affection as much as in unprincipled self-love.
I had already taken to my King Street lodging when I left it for this place.
  PASSAGE: You know I have a horror of new places and a facility in getting over it, which is a double disadvantage in this wandering life of mine; for I am perpetually undergoing the process of feeling miserable and lonely in a new place, and more miserable and lonely still when I leave it.
  context after: The room I have here is gloomy, but opens into my bedroom, which is comfortable, and I shall soon attain the easy liking of habit for it.
Mrs. ----, dear Harriet, is without tact, and learns nothing, which is one reason why, in spite of her many good qualities and accomplishments, I cannot get on with her.

[12] Charles Lamb and Mary Lamb, The Works of Charles and Mary Lamb — Volume 6 Letters 1821-1842 (1775–1834)
  context before: -
  PASSAGE: We are in the House, that is all. I hope one day we shall both enjoy it, and see our friends again.
  context after: But till then I must be a solitary nurse.
I am trying Becky's sister to be with her, so don't say anything to Miss James.

[13] Roe, Frances Marie Antoinette Mack, Army Letters from an Officer's Wife, 1871-1888 (?–1920)
  context before: I feel sorry for the men, but they always march "rout" step and seem to have a good time, for we often hear them laughing and joking with each other.
We are following the Arkansas River, and so far the scenery has been monotonous--just the same rolling plains day after day.
  PASSAGE: Leaving our first army home was distressing, and I doubt if other homes and other friends will ever be quite the same to me.
  context after: Lieutenant Baldwin was assisted to the porch by his faithful Mexican boy, so he could see us start, and he looked white and pitifully helpless, with both arms bandaged tight to his sides. One of those dreadful dogs is in camp and going to Camp Supply with us, and is as frisky as though he had done something to be proud of.

[14] Cécile Tormay, An outlaw's diary: the Commune (1876–1937)
  context before: Little silver buttons glitter on the page’s jacket.
My thoughts fly homeward: in the villages there is still a sense of home, which has long since departed from the towns.
  PASSAGE: I thought of the past winter, the closed shops, the scanty tables. If only I could give that sense of home to somebody....
  context after: And again I feel the glass screen raised between myself and reality.
Mrs. Benjamin Kállay, dressed in white silk, presides over the table.

[15] Hutchins Hapgood, The Autobiography of a Thief (1869–1944)
  context before: I now smoked opium regularly, and had a lay-out in my furnished room and a girl to run it. The drug made me take chances I never used to take; and I became dead to almost everything that was good.
  PASSAGE: I went home very seldom. I liked my family in a curious way, but I did not have enough vitality or much feeling about anything.
  context after: I began to go out to graft always in a dazed condition, so much so that on one occasion a pal tried to take advantage of my state of mind. It was while I was doing a bit of house-work with Sandy and Hacks, two clever grafters.

[16] Frank Thomas Bullen, Recollections The Reminiscences of the Busy Life of One Who Has Played the Varied Parts of Sailor, Author & Lecturer (1857–1915)
  context before: Looking back at those years I am inclined to think so; most people who knew me and what I was doing seemed to think so too; but I, accustomed to the most strenuous physical life and breasting a stormy sea of worry at the same time, felt that it was all play. I think I should have been entirely happy but for the sad fact that I had no home.
  PASSAGE: I was essentially a home-lover, yet I had no home in the true sense of the word.
  context after: More than that I cannot say, except that one day I awoke to the fact that at last and at great cost I had achieved a home and was about to enjoy life as I had never done before. It is true that I was rapidly nearing my jubilee, and that my health was permanently impaired, but--and oh! what a huge but it is--I had emerged into the sunshine and, though that I could not know, ten years of placid joy lay before me.

[17] William Quan Judge and Keightley, Julia Wharton Lewis Campbell Ver Planck, Letters That Have Helped Me (1851–1896)
  context before: One can get wrought up, and then Prana is too strong; so little children sleep much. Be a child once.
  PASSAGE: Well, I'm near home, or rather the centre spot, for pilgrims like you and I have no real house and don't want it; it's too dull and usual for such to want a home.
  context after: And perhaps the little brother is good and well? He shall be ever present, as he always has been, in those little songs and tales told to oneself in the dark, and is, too, the lone warrior seen on the plain of stupid infantry, and he rides a horse whose blood is electricity.

[18] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 2 (1813–1883), translated by Francis Hueffer
  context before: Cordial thanks, dearest Franz, for your kind note, which I had been expecting a long time. The hope which you open to me of seeing you in September is my only light in the night of this sad year.
  PASSAGE: I live here like one of the lost souls in hell. I never thought that I could sink again so low.
  context after: The misery I feel in having to live in these disgusting surroundings is beyond description, and I now realise that it was a sin, a crime, to accept this invitation to London, which in the luckiest case must have led me far away from my real path. I need not expatiate to you upon my actual situation.

[19] John L. Ransom, Andersonville diary (1843–1919)
  context before: Think he was a skulker hiding to keep out of the army, but afraid to hail him. Many of these stay in the woods day-times, and at night go to their homes, getting food.
  PASSAGE: Am now away quite a distance from any habitation, and am afraid those who will look for me cannot find me.
  context after: Occasionally hear shots fired; this is a dangerous locality. Have now been out four days and fared splendidly.

[20] Richard Wagner, My Life — Volume 1 (1813–1883)
  context before: Ere these plans could be carried out, we had still to spend a time of dreadful and acute anxiety, which I shall never forget, within the walls of Magdeburg. It is true I made one more personal attempt in Leipzig to improve my position, on which occasion I entered into the transactions mentioned above with the director of the theatre regarding my new opera.
  PASSAGE: But I soon realised that it was out of the question for me to remain in my native town, and in the disquieting proximity of my family, from which I was restlessly anxious to get away.
  context after: My excitability and depression were noticed by my relations. My mother entreated me, whatever else I might decide to do, on no account to be drawn into marriage while still so young.
```

## Case 5: Drained > stuck

```
(their own words)
  feeling (picked on a feelings wheel): stuck (drained)
  what's happened: I am doing everything I am supposed to do.
  why they think they feel it: none of it feels like it matters
  afraid: that my life has no point
  coping so far: I just keep going through the motions

CANDIDATE PASSAGES
[1] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 1 (1813–1883), translated by Francis Hueffer
  context before: Or shall I look on indifferently, amuse myself when I can make a hundred thalers, buy champagne, and turn my back upon the world? It is a misery.
  PASSAGE: I am going from bad to worse every day, and lead an indescribably worthless life.
  context after: Of real enjoyment of life I know nothing; to me "enjoyment of life, of love," is a matter of imagination, not of experience. In this manner my heart has to go to my brain, and my life becomes an artificial one; only as an "artist" I can live; in the artist my whole "man" has been sunk.

[2] Barbellion, W. N. P. and H. G. Wells, The journal of a disappointed man (1889–1919)
  context before: This continuous preoccupation with self sickens me--as I look back over these entries. It is inconceivable that I should be here steadily writing up my ego day by day in the middle of this disastrous war....
  PASSAGE: Yesterday I had a move on. To-day life wearies me. I am sick of myself and life.
  context after: This beastly world with its beastly war and hate makes me restless, dissatisfied, and full of a longing to be quit of it. I am as full of unrest as an autumn Swallow.

[3] Sarah Bernhardt, Memories of My Life Being My Personal, Professional, and Social Recollections as Woman and Artist (1844–1923)
  context before: Then, too, how many times I accepted invitations to dinner and never went after all, nor did I even send a line of excuse. It is perfectly odious, I know, and yet I always accept with pleasure and intend to go; but when the day comes I am tired, perhaps, or want to have a quiet time, or to be free from any obligation, and when I am obliged to decide one way or another, the time has gone by, and it is too late to send word and too late to go.
  PASSAGE: And so I stay at home, dissatisfied with myself, with everyone else, and with everything.
  context after: Hospitality is a quality made up of primitive taste and antique grandeur. The English are, in my opinion, the most hospitable people on earth, and they are hospitable simply and munificently.

[4] Nathaniel Hawthorne, Passages from the English Notebooks, Volume 1. (1804–1864)
  context before: Nothing gives me any joy. I have learned what the bitterness of exile is, in these days; and I never should have known it but for the absence of "Remote, unfriended, melancholy, slow,"--I can perfectly appreciate that line of Goldsmith; for it well expresses my own torpid, unenterprising, joyless state of mind and heart.
  PASSAGE: I am like an uprooted plant, wilted and drooping. Life seems so purposeless as not to be worth the trouble of carrying it on any further.
  context after: I was at a dinner, the other evening, at Mr. B------'s, where the entertainment was almost entirely American,--New York oysters, raw, stewed, and fried; soup of American partridges, particularly good; also terrapin soup, rich, but not to my taste; American pork and beans, baked in Yankee style; a noble American turkey, weighing thirty-one pounds; and, at the other end of the table, an American round of beef, which the Englishmen present allowed to be delicious, and worth a guinea an ounce. I forget the other American dishes, if there were any more,--O yes! canvas-back ducks, coming on with the sweets, in the usual English fashion.

[5] Catherine Helen Spence, An Autobiography (1825–1910)
  context before: Will no one tell me what it means? I want to find the old unhappy far off things which Wordsworth imagined in the Gaelic song of the 'Highland Lass.'
  PASSAGE: I feel out of it, uneasy, thinking all the time what a poor creature I must be.
  context after: I remember the mother of the sonata players approaching me with beaming countenance on the occasion of one of these performances, expecting the compliment which I faltered forth, doing my best not to look insincere. 'And I have this every evening of my life,' cried the triumphant mother.

[6] Alexander Whyte, Samuel Rutherford and Some of His Correspondents (1836–1921)
  context before: We used to talk in dear old John Meine's back-shop on week-nights and upstairs on Sabbath nights about these things. And long as it is since we saw much of one another, I feel that you know me out and in, and through and through, as no one else knows me.
  PASSAGE: Tell me, then, what I am to do with myself. I will try to do what you tell me, for I am wearied and worn out with my stagnant and miserable life.
  context after: Pity me, Mr. Samuel, my honoured and dear friend, for my pirn is almost run out, and I am not near saved.'
'My worthy and dearly beloved brother in the Lord,' replied Rutherford to Fleming, 'I dare not take it upon me to lay down rules and directions for your inner life.

[7] Mark Twain, Mark Twain's Letters — Volume 4 (1886-1900) (1835–1910)
  context before: DEAR HOWELLS,--I find your generous article in the Weekly, and I want to thank you for its splendid praises, so daringly uttered and so warmly. The words stir the dead heart of me, and throw a glow of color into a life which sometimes seems to have grown wholly wan.
  PASSAGE: I don't mean that I am miserable; no--worse than that--indifferent. Indifferent to nearly everything but work.
  context after: I like that; I enjoy it, and stick to it. I do it without purpose and without ambition; merely for the love of it.

[8] Cook, D. J.‏ ‎, Hands Up; or, Thirty-Five Years of Detective Life in the Mountains and on the Plains Reminiscences by General D. J. Cook, Chief of the Rocky Mountains Detective Association (1840–1907)
  context before: I am glad of it. I am ready and anxious to go with you.
  PASSAGE: I want to get out of this hole, and I am tired of skulking about.
  context after: I would rather a thousand times over go back home and meet all my old-time friends, explain all to them and go to prison, than to go hiding about the country all my life. I could not stand it much longer.

[9] Humphry Ward, A Writer's Recollections — Volume 1 (1851–1920)
  context before: I have no courage for a letter to-day. I have just heard of the horrors of Paris, the burning of the Louvre, the Tuileries, the Hotel de Ville, etc.
  PASSAGE: My heart is wrung. I have energy for nothing. I cannot go out and see people.
  context after: I was in the Bodleian when the Librarian told me this and showed me the newspapers. In presence of such madness and such disasters, they treat a Frenchman here with a kind of pitying sympathy.

[10] Marcus Tullius Cicero, Cicero: Letters to Atticus, Vol. 1 of 3 (107 BC–44 BC), translated by Eric Otto Winstedt
  context before: If he is successful there may very well be some prosecutions. Of that—though to be sure I never despise anything—I’m not much afraid.
  PASSAGE: Everybody is showing me the greatest kindness; but I am sick of life; the whole world is so thoroughly out of joint.
  context after: Just lately we were afraid of a massacre, but it was averted by a speech of that gallant old man Q. Considius: and now the disaster of which we had been in daily fear has suddenly happened. In fact, nothing could be more deplorable than my situation, nothing more enviable than that of Catulus, considering his glorious life and his timely end.

[11] Honoré de Balzac, Letters to Madame Hanska, born Countess Rzewuska, afterwards Madame Honoré de Balzac, 1833-1846 (1799–1850), translated by Katharine Prescott Wormeley
  context before: Make me your bailiff, and you will see that the man who created Grandet understands domestic economy. I would rather be your bailiff than be Lord Byron; Lord Byron was not happy, and I should be very happy.
  PASSAGE: The farther I go, the more frequent are my moments of depression and despair. This solitude and this constant toil without compensation kill me.
  context after: Every day I think back to those days when the person of whom I have told you provisioned me with courage, and shared my labour. What an immense loss!

[12] Madame de Maintenon and of Savoy Marie Adelaide, The Correspondence of Madame, Princess Palatine, Mother of the Regent; of Marie-Adélaïde de Savoie, Duchesse de Bourgogne; and of Madame de Maintenon, in Relation to Saint-Cyr (1635–1719)
  context before: -
  PASSAGE: I grow worse hour by hour, and I suffer day and night; nothing that they do for me relieves me.
  context after: I have great need that God should inspire me with patience; He would do me a great mercy if He delivered me from my sufferings; therefore do not be distressed if you lose me; it will be a great blessing for me.
In addition to my own illness I have another thing that goes to my heart; my poor old Maréchale de Clérembault is very ill.

[13] George Eliot, George Eliot's Life, as Related in Her Letters and Journals. Vol. 1 (of 3) (1819–1880)
  context before: -
  PASSAGE: I am in a miserable state of languor and low spirits, in which everything is a trouble to me.
  context after: I must tell you a bit of Louis Blanc's English, which Mr. Spencer was reciting the other night. The petit homme called on some one, and said, "I come to tell you how you are.

[14] Fanny Kemble, Journal of a Residence on a Georgian Plantation: 1838-1839 (1809–1893)
  context before: Friday, March 1.--Last night after writing so much to you I felt weary, and went out into the air to refresh my spirit. The scene just beyond the house was beautiful, the moonlight slept on the broad river which here is almost the sea, and on the masses of foliage of the great southern oaks; the golden stars of German poetry shone in the purple curtains of the night, and the measured rush of the Atlantic unfurling its huge skirts upon the white sands of the beach (the sweetest and most awful lullaby in nature) resounded through the silent air.
  PASSAGE: I have not felt well, and have been much depressed for some days past. I think I should die if I had to live here.
  context after: This morning, in order not to die yet, I thought I had better take a ride, and accordingly mounted the horse which I told you was one of the equestrian alternatives offered me here; but no sooner did he feel my weight, which, after all, is mere levity and frivolity to him, than he thought proper to rebel, and find the grasshopper a burthen, and rear and otherwise demonstrate his disgust. I have not ridden for a long time now, but Montreal's opposition very presently aroused the Amazon which is both natural and acquired in me, and I made him comprehend that, though I object to slaves, I expect obedient servants; which views of mine being imparted by a due administration of both spur and whip, attended with a judicious combination of coaxing pats on his great crested neck, and endearing commendations of his beauty, produced the desired effect.

[15] Charles Lever, Charles Lever, His Life in His Letters, Vol. II (1806–1872)
  context before: “Croce di Malta, Spezzia, Dec. 30, 1866.
“Your last pleasant note and its ‘stuffing’ has just reached me here, where I am consularising, bullying Custom-house folk, and playing the devil with all the authorities to show my activity in the public service.
  PASSAGE: I can’t endure being away from home and my old routine life; but there was no help for it, and I am here now for another week to come.
  context after: “The name I want for the author of Tony is ‘Arthur Helsham,’ the name of my mother’s family; and the last man who bore the aforesaid was the stupidest blockhead of the house, and the luckiest too. Faustum sit augurium.

[16] Leo Tolstoy, The Journal of Leo Tolstoi (First Volume—1895-1899) (1828–1910), translated by Rose Strunsky
  context before: -
  PASSAGE: I feel that I am alone--that my life not only does not interest any one, but that they are bored and ashamed that I continue to occupy myself with such trifles.
  context after: I thought during this time:
1) A type of woman--there are men such also, but mostly it is women who are incapable of seeing themselves, as if their necks were stationary and they could not look back at themselves.

[17] George Sand and Gustave Flaubert, The George Sand-Gustave Flaubert Letters (1804–1876), translated by Aimée L. McKenzie
  context before: I lose myself in the recollections of my childhood like an old man ... I do not expect anything further in life than a succession of sheets of paper to besmear with black.
  PASSAGE: It seems to me that I am crossing an endless solitude to go I don't know where.
  context after: And it is I who am at the same time the desert, the traveller, and the camel.
I spent the afternoon today at the funeral of Amedee Achard.

[18] Ludwig van Beethoven, Beethoven's Letters 1790-1826, Volume 2 (1770–1827), translated by Lady Grace Wallace
  context before: -
  PASSAGE: I heard of your indisposition with great regret. As for myself, I am often in despair, and almost tempted to put an end to my life, for all these remedies seem to have no end.
  context after: May God have compassion on me, for I look upon myself to be as good as lost! I have a great deal to say to you.

[19] Mrs. Montagu, Elizabeth Montagu, the queen of the bluestockings, Volume 1 (of 2) (1718–1800)
  context before: “He sat next me at the Concert last night; why he is so fond of this place, I cannot tell, for it seems not very agreeable to the nature of a Philosopher.
  PASSAGE: This is a life of idleness and dissipation. I spend great part of my day at home, but most people live upon the Publick Walks.
  context after: I have got up very early and generally read an hour before I go to the Well. The greatest pleasure I have here is riding about to see this wild, rude country.

[20] Hart Crane, The letters of Hart Crane, 1916-1932 (1899–1932)
  context before: My dear Gorham: --/--/ My stand in the drug store has not proved exactly a success, although my father is good enough to admit that I am not to blame in any way. The principal reason that it will be discontinued is that no one can be found to work there without a quite exorbitant salary, and the location is too poor to afford that.
  PASSAGE: So many things have happened lately with the rush of Christmas, etc., that I am tired out and very much depressed today.
  context after: This “affair” that I have been having has been the most intense and satisfactory one of my whole life, and I am all broken up at the thought of leaving him. Yes, the last word will jolt you.
```

## Case 6: Drained > regretful

```
(their own words)
  feeling (picked on a feelings wheel): regretful (drained)
  what's happened: I said something cruel to my brother and now he won't speak to me.
  why they think they feel it: I lost my temper
  afraid: that I have ruined the relationship for good

CANDIDATE PASSAGES
[1] Charlotte Elizabeth, Personal Recollections Abridged, Chiefly in Parts Pertaining to Political and Other Controversies Prevalent at the Time in Great Britain (1790–1846)
  context before: I had an additional motive for continually seeking the Lord, not only in prayer for the enlightening influences of the Holy Spirit on behalf of one so dear, but also for grace to walk most circumspectly myself, lest I should cast any stumbling-block in his way, or give him occasion to suspect that my religious profession was a name, and not a reality. That was surely a profitable idol which kept me always prayerful before God, watchful over myself, diligent in the discharge of duties, and in continual thanksgiving for the mercies I had received.
  PASSAGE: Do I repent loving my brother so well? I wish it had been possible to love him better.
  context after: These warm affections of the heart are among the sweetest relics of a lost Eden, and I would sooner tear up the flowers that God has left to smile in our daily path through a sin-blighted wilderness, far sooner than I would cease to cherish, to foster, to delight in the brighter, sweeter flowers of domestic love, carried to the full extent of all its endearing capabilities.
The Lord knoweth our frame; he deals with us not according to what we are not, but according to what we are.

[2] Margot Asquith, Margot Asquith, an Autobiography - Two Volumes in One (1864–1945)
  context before: I do not think I should mind anything that I have said to others being said to me, but one never can tell; I have a good, sound digestion and personally prefer knowing the truth; I have taken adverse criticism pretty well all my life and had a lot of it; but by some gap I have not succeeded in making my friends take it well. I am not vain or touchy; it takes a lot to offend me; but when I am hurt the scar remains.
  PASSAGE: I feel differently about people who have hurt me; my confidence has been shaken; I hope I am not ungenerous, but I fear I am not really forgiving.
  context after: Worldly people say that explanations are a mistake; but having it out is the only chance any one can ever have of retaining my love; and those who have neither the courage, candour nor humbleness to say they are wrong are not worth loving. I am not afraid of suffering too much in life, but much more afraid of feeling too little; and quarrels make me profoundly unhappy.

[3] Prosper Mérimée, Letters to an Unknown (1803–1870)
  context before: By giving ungraciously, the sacrifice that you are making is deprived of all its merit. You suffer from the pain of this sacrifice all the more keenly because you have not the consolation of knowing that it is appreciated.
  PASSAGE: In your own words, you are suffering a double remorse. I have told you this more than once.
  context after: You accuse me of injustice, but I think the reproach undeserved. You do not judge me fairly.

[4] Frank Thorpe Porter, Twenty Years' Recollections of an Irish Police Magistrate (1801–1882)
  context before: I have a great regard for the collegians; and have always had, and to the last moment of my life I shall remember the kindness with which they have treated me. I thought that a good feeling existed between my men and them, and I think there did.
  PASSAGE: I feel regret for what has occurred--regret that will go down with me to my grave, and I say none but myself alone ought to bear the consequences of what has occurred."
  context after: Mr. M'Donogh--"After that expression of regret, Colonel Browne, I, as a gentleman, shall not ask you another question." (Loud expression of approbation from the students and others present.)

[5] Henry Tracey Coxwell, My life and balloon experiences (1819–1900)
  context before: This incident gave a turn to the fortune of war, and at the real tug which decides so many battles we were again the victors, most unmistakeably so this time, as it became a total rout, and the ringleader was not released until he rendered up his stick and pledged himself never again to oppose or make light of us while exercising.
It was not very long after this scrimmage that a painful circumstance occurred, and as it concerned three of us who had fought in company, and who were shortly after fated to have a difference among ourselves, I may as well mention it at once.
  PASSAGE: I do so with twinges of regret even at this distant period of time, as I was led, almost unwittingly, into a fresh squabble which disfigured, I am aware, my early doings.
  context after: It was in this wise. My brother who was in the last affair (not an elder brother who was in the Royal Navy), had some high words with my colonel, H----, who had led us twice into action as recounted.

[6] Elizabeth Barrett Browning, The Letters of Elizabeth Barrett Browning (Volume 2 of 2) (1806–1861)
  context before: What can you have thought of me? That I was shot or deserved to be?
  PASSAGE: Forgive in the first instance, dearest friend, and believe that I won't behave so any more, if in any way I can help it.
  context after: Tell me your thought now about L. Napoleon. He rode under our windows on December 2 through an immense shout from the Carrousel to the Arc de l'Etoile.

[7] John Keats, Letters to His Family and Friends (1819)
  context before: My dear Rice--Your amende Honorable I must call "un surcroit d'Amitie," for I am not at all sensible of anything but that you were unfortunately engaged and I was unfortunately in a hurry.
  PASSAGE: I completely understand your feeling in this mistake, and find in it that balance of comfort which remains after regretting your uneasiness.
  context after: I have long made up my mind to take for granted the genuine-heartedness of my friends, notwithstanding any temporary ambiguousness in their behaviour or their tongues, nothing of which however I had the least scent of this morning. I say completely understand; for I am everlastingly getting my mind into such-like painful trammels--and am even at this moment suffering under them in the case of a friend of ours.--I will tell you two most unfortunate and parallel slips--it seems down-right pre-intention--A friend says to me, "Keats, I shall go and see Severn this week."--"Ah! (says I) you want him to take your Portrait."--And again, "Keats," says a friend, "when will you come to town again?"--"I will," says I, "let you have the MS. next week."

[8] William Quan Judge and Keightley, Julia Wharton Lewis Campbell Ver Planck, Letters That Have Helped Me (1851–1896)
  context before: In you, as now you exist, lies all the past. So follow the Hindu maxim: "Regret nothing; never be sorry; and cut all doubts with the sword of spiritual knowledge."
  PASSAGE: Regret is productive only of error. I care not what I was, or what any one was.
  context after: I only look for what I am each moment. For as each moment is and at once is not, it must follow that if we think of the past we forget the present, and while we forget, the moments fly by us, making more past.

[9] William Makepeace Thackeray, The Fitz-Boodle Papers (1811–1863)
  context before: I have been sitting for two hours since I marked the asterisks, thinking--thinking. I have committed crimes in my life--who hasn't?
  PASSAGE: But talk of remorse, what remorse is there like THAT which rushes up in a flood to my brain sometimes when I am alone, and causes me to blush when I'm a-bed in the dark?
  context after: I fell, sir, on that infernal slippery floor. Down we came like shot; we rolled over and over in the midst of the ballroom, the music going ten miles an hour, 800 pairs of eyes fixed upon us, a cursed shriek of laughter bursting out from all sides.

[10] Ida M. Tarbell, All in the Day's Work: An Autobiography (1857–1944)
  context before: Perhaps it was just as well, both for McClure’s and for me. Repeating yourself is a doubtful practice, particularly for editor and writer.
  PASSAGE: I feel now there was no hope of my recapturing the former interest in the former way.
  context after: The result would have smelt a bit musty. Indeed, though I hate to admit it, I think there has been a slight mustiness about all I have done in the nineteen years since I started “on my own”—that is, not on assignment—built as it has been on work done before the Great War.

[11] Benjamin Franklin, Memoirs of Benjamin Franklin; Written by Himself. [Vol. 1 of 2] With His Most Interesting Essays, Letters, and Miscellaneous Writings; Familiar, Moral, Political, Economical, and Philosophical, Selected with Care from All His Published Productions, and Comprising Whatever Is Most Entertaining and Valuable to the General Reader (1706–1790)
  context before: Thus it was that I made my brother ample amends for the service I had deprived him of by leaving him so early.
In 1736 I lost one of my sons, a fine boy of four years old, by the smallpox, taken in the common way.
  PASSAGE: I long regretted him bitterly, and still regret that I had not given it to him by inoculation.
  context after: This I mention for the sake of parents who omit that operation, on the supposition that they should never forgive themselves if a child died under it; my example showing that the regret may be the same either way, and, therefore, that the safer should be chosen.
Our club, the Junto, was found so useful, and afforded such satisfaction to the members, that some were desirous of introducing their friends, which could not well be done without exceeding what we had settled as a convenient number, viz., twelve.

[12] W. H. Davies and Bernard Shaw, The Autobiography of a Super-Tramp (1871–1940)
  context before: My grandfather would most certainly have paid a fine of twenty or thirty pounds to save me from punishment, and offered, I believe, to do the same. Alas! the magistrates were inexorable, and I and my lieutenant were sentenced each to twelve strokes with the birch rod, whilst the other four, not being caught red-handed, received six strokes each.
  PASSAGE: I do not at present feel much remorse for those desperate times, but often think of the disgrace to parents.
  context after: The kindly admonishment of my schoolmaster made me shed the real tears of repentance, not being forced from me by any thought of punishment. This ended my schooldays; and after the breaking up of our gang, I was not allowed much liberty, our elders being afraid of a reorganisation.

[13] Goethe, Johann Wolfgang von, Autobiography: Truth and Fiction Relating to My Life (1749–1832), translated by John Oxenford
  context before: I asserted, finally, that I had nothing more to say, and well knew that I need fear nothing, for I was innocent, of a good family, and well reputed; but that they might be just as guiltless without having it recognized, or being otherwise favored. I declared at the same time, that if they were not spared like myself, that if their follies were not regarded with indulgence, and their faults pardoned, that if any thing in the least harsh or unjust happened to them, I would do some violence to myself, and no one should prevent me.
  PASSAGE: In this, too, my friend tried to pacify me; but I did not trust him, and was, when he quitted me at last, in a most terrible state.
  context after: I now reproached myself for having told the affair, and brought all the positions to light. I foresaw that our childlike actions, our youthful inclinations and confidences, would be quite differently interpreted, and that I might perhaps involve the excellent Pylades in the matter, and render him very unhappy.

[14] Henry James, The Letters of Henry James (Vol. II) (1843–1916)
  context before: I won't go into the history of my woes--all the more that I really hope I have shuffled the worst of them off. Even in this most recent form they have been part and parcel of the grave illness that overtook me as long ago as at the New Year, 1910, and with a very imperfect recovery from which I was struggling during those weary American months of winter-before-last when we planned so in vain that I should come to you in Washington.
  PASSAGE: I have deeply regretted, ever since, my failure of that pleasure--all the more that I don't see it now as conceivably again within my reach.
  context after: I am restored to this soil, for whatever may remain to me of my mortal career. The grand swing across the globe, which you and Harry will again nobly accomplish--again and yet again--now simply mocks at my weakness and my reduced resources.

[15] George Fox, George Fox: An Autobiography (1624–1691)
  context before: I wondered why these things should come to me. I looked upon myself, and said, "Was I ever so before?"
  PASSAGE: Then I thought, because I had forsaken my relations I had done amiss against them.
  context after: So I was brought to call to mind all my time that I had spent, and to consider whether I had wronged any; but temptations grew more and more, and I was tempted almost to despair; and when Satan could not effect his design upon me that way, he laid snares and baits to draw me to commit some sin, whereof he might take advantage to bring me to despair.
I was about twenty years of age when these exercises came upon me; and some years I continued in that condition, in great trouble; and fain I would have put it from me.

[16] Robert Burns, Letters (1790)
  context before: A Mrs. G--, a charming woman, did me the honour to be prejudiced in my favour; this makes me hope that I have not outraged her beyond all forgiveness.--To all the other ladies please present my humblest contrition for my conduct, and my petition for their gracious pardon. O all ye powers of decency and decorum! whisper to them that my errors, though great, were involuntary--that an intoxicated man is the vilest of beasts--that it was not in my nature to be brutal to any one--that to be rude to a woman, when in my senses, was impossible with me--but--
  PASSAGE: Regret! Remorse! Shame! ye three hell hounds that ever dog my steps and bay at my heels, spare me! spare me!
  context after: Forgive the offences, and pity the perdition of, Madam, your humble slave,

[17] Leo Tolstoy, The Journal of Leo Tolstoi (First Volume—1895-1899) (1828–1910), translated by Rose Strunsky
  context before: My heart aches without stopping. I continue to suffer and can not subject myself to God....
  PASSAGE: I have not mastered pride and rebellion and the pain in my heart does not stop.
  context after: One thing consoles me; I am not alone but with God, and therefore no matter how painful it is, yet I feel that something is taking place within me. Help me, Father.

[18] Amelia E. Barr, All the Days of My Life: An Autobiography The Red Leaves of a Human Heart (1831–1919)
  context before: I had been only half-hearted about the movement, for it appeared to put the Astor Library too far from me. But the children were delighted with the change, and the human heart is a loving thing, and has reasons that reason does not understand.
  PASSAGE: And I had not then learned that a little misgiving in the beginning of things, means much regret in the end of them.
  context after: The first change necessary in our lives was that Mary or Lilly should do the office work. One of them went to the city with me nearly every morning.

[19] Arthur Christopher Benson, The Upton Letters (1862–1925)
  context before: But one ought not, I confess, to be so wedded to one's own habits; and I feel, when I complain, rather like the rich gentleman who said to John Wesley, when his fire smoked, "These are some of the crosses, Mr. Wesley, that I have to bear."
I could have stood it with more equanimity if only Mr. Welbore had been a congenial guest.
  PASSAGE: But even in the brief time at my disposal I grew to dislike him with an intensity of which I am ashamed.
  context after: I hated his clothes, his boots, his eye-glass, the way he cleared his throat, the way he laughed. He is a successful, downright, blunt, worldly man, and is generally called a good fellow by his friends.

[20] Mary Wollstonecraft and William Godwin, Memoirs and Posthumous Works of Mary Wollstonecraft Godwin, Vol. 1 (1759–1797)
  context before: Ah! ask yourself if you have not condescended to employ a little address, I could almost say cunning, unworthy of you?—Principles are sacred things—and we never play with truth, with impunity.
The expectation (I have too fondly nourished it) of regaining your affection, every day grows fainter and fainter.—Indeed it seems to me, when I am more sad than usual, that I shall never see you more.—Yet you will not always forget me.
  PASSAGE: You will feel something like remorse, for having lived only for yourself—and sacrificed my peace to inferior gratifications.
  context after: In a comfortless old age, you will remember that you had one disinterested friend, whose heart you wounded to the quick. The hour of recollection will come—and you will not be satisfied to act the part of a boy, till you fall into that of a dotard.
```

## Case 7: On edge > anxious

```
(their own words)
  feeling (picked on a feelings wheel): anxious (on edge)
  what's happened: My rent has gone up again and I am already in my overdraft.
  why they think they feel it: I cannot see how I will pay
  afraid: that I will lose my home

CANDIDATE PASSAGES
[1] Marcus Tullius Cicero, Letters of Marcus Tullius Cicero (107 BC–44 BC), translated by Evelyn S. Shuckburgh
  context before: There is a threat of a Parthian war. Cassius's despatch was empty brag: that of Bibulus had not arrived: when that is read I think the senate will at length be roused.
  PASSAGE: I am myself in serious anxiety. If, as I hope, my government is not prolonged, I have only June and July to fear.
  context after: May it be so! Bibulus will keep them in check for two months.

[2] Ian Hamilton, Gallipoli Diary, Volume 2 (1853–1947)
  context before: The memory of Cromwell prevails over that of Prince Rupert with most Englishmen but Prince Rupert, per se, usually prevailed over Cromwell. To your adventurous soldier; to our heroes, Bobs, Sir Evelyn, Garnet Wolseley, Charles Gordon (great psalm-singer though he was) an occasion like to-night's holds the same intoxicating mixture of danger and desire as fills the glass of the boy bridegroom when he raises it to the health of his enigma in a veil.
  PASSAGE: But I don't know how it is; I used to feel like that; now I too am terribly anxious.
  context after: Disappointed not to see Stopford nor Reed. They were to have been there.

[3] Honoré de Balzac, Letters to Madame Hanska, born Countess Rzewuska, afterwards Madame Honoré de Balzac, 1833-1846 (1799–1850), translated by Katharine Prescott Wormeley
  context before: MADAME,--If it were not that I get impatient and suffer at losing so much time, both for that which gives me pleasure and also for my work, I should be this morning well, and like a man who has had a fever.
  PASSAGE: I don't know whether I had better go out or keep my room; but I frankly own that here, alone, I worry horribly.
  context after: A thousand thanks for your good care, and forgive me that, yesterday, I was more surprised than grateful at your visit, which touched me deeply after you had left. I don't know if you know that there are things that get stronger as they get older.

[4] Elizabeth Barrett Browning, The Letters of Elizabeth Barrett Browning (Volume 2 of 2) (1806–1861)
  context before: -
  PASSAGE: I am anxious about America, fearing a compromise in the North. All other dangers are comparatively null.
  context after: * * * * *
To Miss E.F. Haworth

[5] Edward Gibbon, Private Letters of Edward Gibbon (1753-1794) Volume 2 (of 2) (1737–1794)
  context before: All reasonable chances are in favour of a confederacy, such as was never opposed to the ambition of Louis XIV.; but, after the experience of last year, I distrust reason, and confess myself fearful for the event. The French are strong in numbers, activity, enthusiasm; they are rich in rapine; and although their strength may be only that of a frenzy-feaver, they may do infinite mischief to their neighbours before they can be reduced to a strait wastecoat.
  PASSAGE: I dread the effects that may be produced on the minds of the people by the increase of debt and taxes, probable losses, and possible mismanagement.
  context after: Our trade must suffer; and though projects of invasion have been always abortive, I cannot forget that the fleets and armies of Europe have failed before the towns in America, which have been taken and plundered by a handful of Buccaneers. I know nothing of Pitt as a War Minister; but it affords me much satisfaction that the intrepid wisdom of the new Chancellor is introduced into the Cabinet.

[6] Lucie Duff Gordon, Letters from Egypt (1821–1869)
  context before: The horror of killing seems greater here than ever I saw it. Palgrave says the same of the Arabian Arabs in his book: it is not one's notion of Oriental feeling, but a murder in England is taken quite as a joke compared with the scene here.
  PASSAGE: I fear there will be robberies, owing to the distress, and the numbers who are running away from the land unable to pay their taxes.
  context after: Don't fear for me, for I have two watchmen in the house every night--the regular guard and an amateur, a man whose boy I took down to Cairo to study in Gama'l Azhar.
Palgrave has written to Ross wanting Mabrook back.

[7] Prosper Mérimée, Letters to an Unknown (1803–1870)
  context before: I am too old and too ill to undertake another such journey. If I did not feel in duty bound to go bidding good-bye to some of my best friends, I should not budge from my hole.
  PASSAGE: While I am not ill, I am so nervous that it is worse than illness.
  context after: I neither eat nor sleep, and have, besides, the blue devils. My only consolation is the knowledge that you are enjoying yourself, and are rapidly gaining in flesh among your mountains and country-folk.

[8] John Adams and Abigail Adams, Familiar Letters of John Adams and His Wife Abigail Adams During the Revolution with a Memoir of Mrs. Adams (1735–1826)
  context before: The more distinguished the person, the greater the inveteracy of these foes of human nature. The argument of my friends to alleviate my anxiety, by persuading me that this shocking attempt will put you more upon your guard and render your person more secure than if it had never taken place, is kind in them, and has some weight; but my greatest comfort and consolation arise from the belief of a superintending Providence, to whom I can with confidence commit you, since not a sparrow falls to the ground without his notice.
  PASSAGE: Were it not for this, I should be miserable and overwhelmed by my fears and apprehensions.
  context after: Freedom of sentiment, the life and soul of friendship, is in a great measure cut off by the danger of miscarriage and the apprehension of letters falling into the hands of our enemies. Should this meet with that fate, may they blush for their connection with a nation who have rendered themselves infamous and abhorred by a long list of crimes, which not their high achievements, nor the lustre of former deeds, nor the tender appellation of parent, nor the fond connection which once subsisted, can ever blot from our remembrance, nor wipe out those indelible stains of their cruelty and baseness.

[9] Francis Leopold M'Clintock and Roderick Impey Murchison, In the Arctic Seas A Narrative of the Discovery of the Fate of Sir John Franklin and his Companions (1819–1907)
  context before: A wintry night, much wind and snow.
19th.--Continued strong S.E. winds, pressing the ice closely together, dark sky and snow; everything wears a wintry and threatening aspect; we are closely hemmed in, and have our rudder and screw unshipped.
  PASSAGE: This recommencement of S.E. winds and rapid ebbing of the small remaining portion of summer makes me more anxious about the future than the present.
  context after: Yesterday the weather improved, and by working for thirteen hours we got the ship out of her small ice-creek into a larger space of water, and in so doing advanced a mile and a half. It is now calm, but the ice still drifts, as we would wish it, to the N.W. Yesterday we were within 12 miles of the position of the 'Enterprise' upon the same day in 1848, and under very similar conditions of weather and ice also.

[10] Sarah Morgan Dawson, A Confederate Girl's Diary (1842–1909)
  context before: -
  PASSAGE: I am afraid I shall be nervous when the moment of the bombardment actually arrives.
  context after: This suspense is not calculated to soothe one's nerves. A few moments since, a salute was fired in honor of General Butler's arrival, when women, children, and servants rushed to the front of the houses, confident of a repetition of the shelling which occurred a month ago to-day.

[11] Samuel Pepys, Diary of Samuel Pepys — Volume 45: August/September 1666 (1633–1703), translated by Mynors Bright
  context before: I saw him on Saturday, after his fit of the ague, and then was pretty lusty. Which troubles me mightily, for he is a very good, harmless, honest gentleman, though not fit for the business.
  PASSAGE: But I much fear a worse may come, that may be more uneasy to me.
  context after: Up, and to Deptford by water, reading "Othello, Moore of Venice," which I ever heretofore esteemed a mighty good play, but having so lately read "The Adventures of Five Houres," it seems a mean thing. Walked back, and so home, and then down to the Old Swan and drank at Betty Michell's, and so to Westminster to the Exchequer about my quarter tallies, and so to Lumbard Streete to choose stuff to hang my new intended closet, and have chosen purple.

[12] Mark Twain, Mark Twain's Letters — Volume 2 (1867-1875) (1835–1910)
  context before: MY DEAR MRS. HOWELLS,--Don't dream for one instant that my not getting a letter from you kept me from Boston.
  PASSAGE: I am too anxious to go to let such a thing as that keep me.
  context after: Mr. Clemens did have such a good time with you and Mr. Howells. He evidently has no regret that he did not get to the Centennial.

[13] Charles Dickens, The Letters of Charles Dickens. Vol. 2, 1857-1870 (1812–1870)
  context before: After a very anxious consultation with Forster, and careful heed of what is to be said for and against, I have made up my mind to see it out. I do not expect as much money as the calculators estimate, but I cannot set the hope of a large sum of money aside.
  PASSAGE: I am so nervous with travelling and anxiety to decide something, that I can hardly write.
  context after: But I send you these few words as my dearest and best friend.

[14] Amy Fay, Music-Study in Germany, from the Home Correspondence of Amy Fay (1844–1928)
  context before: It is a fearful day's work every time I go to him. First, four hours' practice in the morning.
  PASSAGE: Then a nervous, anxious feeling that takes away my appetite, and prevents me from eating my dinner.
  context after: And then several hours at Liszt's, where one succession of concertos, fantasias, and all sorts of tremendous things are played. You never know before whom you must play there, for it is the musical headquarters of the world.

[15] Richard Harding Davis, Adventures and Letters of Richard Harding Davis (1864–1916)
  context before: That man of war, for instance, was the only American one that had touched at Puerto Cortez in TEN years and it came the day we did and left the day we did. We saw a big lithograph of Eddie Sothern in a palm hut here so we went before a notary and swore to it and had three seals put on the paper and sent it him as a joke.
  PASSAGE: We start tomorrow the 22nd so you see we are behind our schedule and I suppose you people are all worried to death about us.
  context after: We will be much longer than six days on our way to Tegucigalpa as we are going shooting and also to pay our respects to Bogran the ex-president and the man who is getting up the next revolution. But we take care to tell everyone we are travelling for pleasure and are great admirers of Bonilla the present president.

[16] Sarah Bernhardt, Memories of My Life Being My Personal, Professional, and Social Recollections as Woman and Artist (1844–1923)
  context before: At last the change took place, and the serious rehearsals commenced. Then the first performance was announced for November 6 (1872).
  PASSAGE: I have always had, from the very beginning, and still have, a terrible fear, especially when I know that much is expected from me.
  context after: And I knew a long time beforehand that the Salle had been let; I knew that the Press counted on a big success, and that Perrin himself was reckoning on a succession of good takings.
Alas! all these hopes and predictions went for nothing, and my débuts at the Comédie Française were only mediocre.

[17] Barbellion, W. N. P. and H. G. Wells, The journal of a disappointed man (1889–1919)
  context before: -
  PASSAGE: Have had a relapse. My hand I fear is going. Food prices are leaping up.
  context after: Woe to the unfit and the old and the poor in these coming days! We shall soon have nothing left in our pantries, and a piece of Wrigley's chewing gum will be our only comfort.

[18] Charles Darwin, More Letters of Charles Darwin — Volume 1 A Record of His Work in a Series of Hitherto Unpublished Letters (1809–1882)
  context before: It gives me a demoniacal chuckle to think of Owen's pleasant countenance when he reads it.
I have not been in London since the end of September; when I do come I will beat up your quarters if I possibly can; but I do not know what has come over me.
  PASSAGE: I am worse than ever in bearing any excitement. Even talking of an evening for less than two hours has twice recently brought on such violent vomiting and trembling that I dread coming up to London.
  context after: I hear that you came out strong at Cambridge (145/5. Prof. Owen, in a communication to the British Association at Cambridge (1862) "On a tooth of Mastodon from the Tertiary marls, near Shanghai," brought forward the case of the Australian Mastodon as a proof of the remarkable geographical distribution of the Proboscidia.

[19] Anton Chekhov, Letters to His Family and Friends (1890), translated by Constance Garnett
  context before: If without finishing my novel I take another thousand roubles for the tour abroad, and then for living after the tour, I shall get into such a tangle that the devil himself could not pull me out by the ears. I am not in a tangle yet because I am up to all sorts of dodges, and live more frugally than a mouse; but if I go abroad everything will go to the devil.
  PASSAGE: My accounts will be in a mess and I shall get myself hopelessly in debt.
  context after: The very thought of a debt of two thousand makes my heart sink.
There are other considerations, but they are all of small account beside that of money and work.

[20] Acton, John Emerich Edward Dalberg Acton, Letters of Lord Acton to Mary, Daughter of the Right Hon. W. E. Gladstone (1834–1902)
  context before: -
  PASSAGE: We have nothing later than Tuesday's speech, so that the lines are not traceable into the future, and I am still in a very anxious and doubting stage.
  context after: -
```

## Case 8: On edge > unsure what's next

```
(their own words)
  feeling (picked on a feelings wheel): unsure what's next (on edge)
  what's happened: The doctor wants more tests.
  why they think they feel it: it might be something serious
  afraid: that I might not have much time

CANDIDATE PASSAGES
[1] Jonathan Swift, The Journal to Stella (1667–1745)
  context before: I hope in some time they will be persuaded here to give me some money to pay off these debts. I must finish the book I am writing, {545b} before I can go over; and they expect I shall pass next winter here, and then I will dun them to give me a sum of money.
  PASSAGE: However, I hope to pass four or five months with MD, and whatever comes on it.
  context after: MD’s allowance must be increased, and shall be too, fais . . . {545c} I received oor rettle No. 39 to-night; just ten weeks since I had your last. I shall write next post to Bishop Sterne.

[2] Prosper Mérimée, Letters to an Unknown (1803–1870)
  context before: I am too old and too ill to undertake another such journey. If I did not feel in duty bound to go bidding good-bye to some of my best friends, I should not budge from my hole.
  PASSAGE: While I am not ill, I am so nervous that it is worse than illness.
  context after: I neither eat nor sleep, and have, besides, the blue devils. My only consolation is the knowledge that you are enjoying yourself, and are rapidly gaining in flesh among your mountains and country-folk.

[3] Sarah Morgan Dawson, A Confederate Girl's Diary (1842–1909)
  context before: Clinton, at least, I am sure of. Lilly came down for me yesterday, and according to the present programme, though I will not answer for it in an hour from now, we leave Linwood this evening, and Clinton on Thursday.
  PASSAGE: I am almost indifferent about our destination; my chief anxiety is to have some definite plans decided on, which seems perfectly impossible from the number of times they are changed a day.
  context after: The uncertainty is really affecting my spine, and causing me to grow alarmingly thin....

[4] Marcus Tullius Cicero, Cicero: Letters to Atticus, Vol. 3 of 3 (107 BC–44 BC), translated by Eric Otto Winstedt
  context before: That would not disturb me much, if it were not that somehow or other, perhaps without any good reason, I should be sorry for it to be called anything but a shrine. If I want that, I'm afraid I can't have it, unless I change the site.
  PASSAGE: Please consider what there is in this point. For though I am less anxious and have almost recovered myself, still I want your advice.
  context after: So I entreat you with more urgency than you wish or allow me to use, to give your whole mind to considering this question.

[5] Arthur Young, The autobiography of Arthur Young (1741–1820)
  context before: It is surely incumbent on you to consider, that when a father is doing everything upon earth for your good, yet you ought from feelings of gratitude and generosity to do all you can for yourself. I ask nothing but what another would positively insist on, and would order violent means of securing obedience; I, on the contrary, rely on your own feelings and your good sense, and so relying, I do beg that you will take everything ordered without murmur or hesitation, for I assure you it is with astonishment I hear that you have omitted this some time.
  PASSAGE: Call your understanding to your aid, and ask yourself what you can think must be my surprise at hearing that while all around you are anxious for your health, that you alone will be careless of it.
  context after: It is a much worse thing than ill health, for I had rather hear you were worse in body than that you had a malady in your heart or head. Think seriously of such conduct, and I am confident it will cease, for I know your disposition, and that makes me the more surprised, for knowing your good temper so well as I do it is perfectly astonishing.

[6] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 2 (1813–1883), translated by Francis Hueffer
  context before: You must come soon, if POSSIBLE this SPRING. I feel that on our meeting this time everything, everything depends.
  PASSAGE: I am continually at war with my health, and fear a relapse at every moment.
  context after: But let us leave this for today. We shall soon meet.

[7] Helen Keller, The Story of My Life With her letters (1887-1901) and a supplementary account of her education, including passages from the reports and letters of her teacher, Anne Mansfield Sullivan, by John Albert Macy (1880–1968)
  context before: CHARLES T. COPELAND December 20, 1900. My dear Mr. Copeland; I venture to write to you because I am afraid that if I do not explain why I have stopped writing themes, you will think I have become discouraged, or perhaps that to escape criticism I have beat a cowardly retreat from your class.
  PASSAGE: Please do not think either of these very unpleasant thoughts. I am not discouraged, nor am I afraid.
  context after: I am confident that I could go on writing themes like those I have written, and I suppose I should get through the course with fairly good marks; but this sort of literary patch-work has lost all interest for me. I have never been satisfied with my work; but I never knew what my difficulty was until you pointed it out to me.

[8] Honoré de Balzac, Letters to Madame Hanska, born Countess Rzewuska, afterwards Madame Honoré de Balzac, 1833-1846 (1799–1850), translated by Katharine Prescott Wormeley
  context before: Do not be surprised at the number of days since I have written to you. This interruption is due to the sharpness of the conflict, the necessity of a work that takes days and nights.
  PASSAGE: I am in fear of succumbing. Also, events have become very serious in my family.
  context after: Something had to be done about my brother,--get him off to India, or induce him to go.
You, so little concerned about money, you will never know, until I relate them to you by the fireside in your steppe, the difficulties there are in paying ten thousand francs a month, without other resource than one's pen.

[9] Robert E. Lee, Recollections and Letters of General Robert E. Lee (1843–1914)
  context before: Should nothing prevent, I will leave here to-morrow, but I fear I shall not be able to reach the Rockbridge Alum, which I am told is twenty-nine miles distant. In that event, I will halt on the road, and arrive there on Saturday, lie over Sunday, and reach Lexington on Monday.
  PASSAGE: I am very anxious to get to Lexington, and think nothing on the route will benefit me, as I feel much concerned about the resumption of the college exercises.
  context after: Mr. John Stewart, Misses Mary and Marian, Mr. Price, and his daughters came over from the Hot yesterday to see me. The Stewarts are there on Miss Belle’s account.

[10] Acton, John Emerich Edward Dalberg Acton, Letters of Lord Acton to Mary, Daughter of the Right Hon. W. E. Gladstone (1834–1902)
  context before: -
  PASSAGE: We have nothing later than Tuesday's speech, so that the lines are not traceable into the future, and I am still in a very anxious and doubting stage.
  context after: -

[11] Robert Browning and Elizabeth Barrett Browning, The letters of Robert Browning and Elizabeth Barrett Barrett, Vol. 1 (of 2) 1845-1846 (1812–1889)
  context before: It appears that the direct Leghorn steamer will not sail on the third, and may not until the middle of October, and if forced to still further delay, which is possible, will not at all. One of my brothers has been to Mr. Andrews of St. Mary Axe and heard as much as this.
  PASSAGE: What shall I do? The middle of October, say my sisters ... and I half fear that it may prove so ... is too late for me--to say nothing for the uncertainty which completes the difficulty.
  context after: On the 20th of September (on the other hand) sails the Malta vessel; and I hear that I may go in it to Gibraltar and find a French steamer there to proceed by. Is there an objection to this--except the change of steamers ... repeated ... for I must get down to Southampton--and the leaving England so soon?

[12] Ian Hamilton, Gallipoli Diary, Volume 2 (1853–1947)
  context before: The memory of Cromwell prevails over that of Prince Rupert with most Englishmen but Prince Rupert, per se, usually prevailed over Cromwell. To your adventurous soldier; to our heroes, Bobs, Sir Evelyn, Garnet Wolseley, Charles Gordon (great psalm-singer though he was) an occasion like to-night's holds the same intoxicating mixture of danger and desire as fills the glass of the boy bridegroom when he raises it to the health of his enigma in a veil.
  PASSAGE: But I don't know how it is; I used to feel like that; now I too am terribly anxious.
  context after: Disappointed not to see Stopford nor Reed. They were to have been there.

[13] Robert Burns, Letters (1790)
  context before: Solitary confinement, you know, is Howard's favourite idea of reclaiming sinners; so let me consider by what fatality it happens, that I have so long been exceeding sinful as to neglect the correspondence of the most valued friend I have on earth. To tell you that I have been in poor health will not be excuse enough, though it is true.
  PASSAGE: I am afraid that I am about to suffer for the follies of my youth.
  context after: My medical friends threaten me with a flying gout; but I trust they are mistaken.
I am just going to trouble your critical patience with the first sketch of a stanza I have been framing, as I passed along the road.

[14] Napoleon I, Emperor of the French, Napoleon's Letters to Josephine, 1796-1812 For the First Time Collected and Translated, with Notes Social, Historical, and Chronological, from Contemporary Sources (1769–1821)
  context before: Where I make war, here or there, is a matter of indifference. To serve my country, to deserve from posterity a page in our history, to give the Government proofs of my attachment and devotion--that is the sum of my ambition.
  PASSAGE: But I am very anxious not to lose in a week the fatigues, anxieties, and dangers of two months, and to find myself fettered.
  context after: I began with a certain amount of fame; I wish to continue worthy of you." To the Directory he writes that the expeditions to Leghorn, Rome, and Naples are small affairs, but to be safely conducted must have one general in command.

[15] Charles Dickens, The Letters of Charles Dickens. Vol. 2, 1857-1870 (1812–1870)
  context before: After a very anxious consultation with Forster, and careful heed of what is to be said for and against, I have made up my mind to see it out. I do not expect as much money as the calculators estimate, but I cannot set the hope of a large sum of money aside.
  PASSAGE: I am so nervous with travelling and anxiety to decide something, that I can hardly write.
  context after: But I send you these few words as my dearest and best friend.

[16] Ford Madox Brown and Dante Gabriel Rossetti, Præraphaelite diaries and letters (1821–1893)
  context before: How little done, O Lord, and how much gone through! How many changes, how many failures!
  PASSAGE: Is it fate, is it fault? Will it end, or must it end me? A bad cold on my chest with pain therein these three days.
  context after: 17th.--Up at half-past nine--to work at the sketch as before from eleven till six; unsatisfactory. To-night accounts, also unsatisfactory.

[17] Charlotte Biggs, A Residence in France During the Years 1792, 1793, 1794 and 1795, Part II., 1793 Described in a Series of Letters from an English Lady: with General and Incidental Remarks on the French Character and Manners (1763–1827)
  context before: After breakfasting together, and conversing on very civil terms, Dumont told him, that as he concerned himself so much in behalf of his friend, he would send him to keep the latter company, and at the conclusion of his visit he was sent prisoner to the Bicetre.
Perhaps the greater part of between three and four hundred thousand people, now imprisoned on suspicion, have been arrested for reasons as little substantial.
  PASSAGE: --I begin to fear my health will not resist the hardship of a long continuance here.
  context after: We have no fire-place, and are sometimes starved with partial winds from the doors and roof; at others faint and heartsick with the unhealthy air produced by so many living bodies. The water we drink is not preferable to the air we breathe; the bread (which is now every where scarce and bad) contains such a mixture of barley, rye, damaged wheat, and trash of all kinds, that, far from being nourished by it, I lose both my strength and appetite daily.--Yet these are not the worst of our sufferings.

[18] Anton Chekhov, Letters to His Family and Friends (1890), translated by Constance Garnett
  context before: In the second, he has a large dose of cowardice. Looking towards the future I call nothing but cowardice.
  PASSAGE: I am afraid of getting into a muddle, and every journey complicates my financial position.
  context after: No, don’t tempt me without need. Don’t write to me of the sea.

[19] Hart Crane, The letters of Hart Crane, 1916-1932 (1899–1932)
  context before: Dear Waldo: --/--/ These are bewildering times for everyone, I suppose. I can’t muster much of anything to say to anyone.
  PASSAGE: I seem to have lost the faculty to even feel tension. A bad sign, I’m sure.
  context after: When they all get it decided, Capitalism or Communism, then I’ll probably be able to resume a few intensities; meanwhile there seems to be no sap in anything. I’d love to fight for--almost anything, but there seems to be no longer any real resistance.

[20] Simon Newcomb, The Reminiscences of an Astronomer (1835–1909)
  context before: I felt its importance at the time. As I walked and walked, the question in my mind was, what am I doing and whither am I going?
  PASSAGE: Am I doing right or wrong? Am I going forward to success in life, or to failure and degradation?
  context after: Vainly, vainly, I tried to peer into the thick darkness of the future. No definite idea of what success might mean could find a place in my mind.
```

## Case 9: Small > not good enough

```
(their own words)
  feeling (picked on a feelings wheel): not good enough (small)
  what's happened: Everyone I know is getting promoted or engaged.
  why they think they feel it: I am stuck where I was
  afraid: that I am falling behind for good

CANDIDATE PASSAGES
[1] Anthony Trollope, An Autobiography of Anthony Trollope (1815–1882)
  context before: I do not think that the failure--for it did fail--arose from bad editing. Perhaps too much editing might have been the fault.
  PASSAGE: I was too anxious to be good, and did not enough think of what might be lucrative.
  context after: It did fail, for it never paid its way. It reached, if I remember right, a circulation of nearly 10,000--perhaps on one or two occasions may have gone beyond that.

[2] Andrew Dickson White, Autobiography of Andrew Dickson White — Volume 2 (1832–1918)
  context before: On my endeavoring to retain him, he answered as follows: "I have been over twelve years in the American diplomatic service as secretary; I have seen the secretaries here, from all other countries, steadily promoted until all of them still remaining in the service are in higher posts, several of them ministers, and some ambassadors. I remain as I was at the beginning, with no promotion, and no probability of any.
  PASSAGE: I feel that, as a rule, my present colleagues, as well as most officials with whom I have to do, seeing that I have not been advanced, look upon me as a failure.
  context after: They cannot be made to understand how a man who has served so long as secretary has been denied promotion for any reason save inefficiency. I can no longer submit to be thus looked down upon, and I must resign."

[3] Henri Frédéric Amiel, Amiel's Journal: The Journal Intime of Henri-Frédéric Amiel (1821–1881), translated by Mrs. Humphry Ward
  context before: (Hyères.)--In spite of my sleeping draught I have had a bad night. Once it seemed as if I must choke, for I could breathe neither way.
  PASSAGE: Could I be more fragile, more sensitive, more vulnerable! People talk to me as if there were still a career before me, while all the time I know that the ground is slipping from under me, and that the defense of my health is already a hopeless task.
  context after: At bottom, I am only living on out of complaisance and without a shadow of self-delusion. I know that not one of my desires will be realized, and for a long time I have had no desires at all.

[4] Mrs. Montagu, Elizabeth Montagu, the queen of the bluestockings, Volume 2 (of 2) (1718–1800)
  context before: The Bible alone will make a good man; human learning without the fear of God, which is the beginning of Wisdom and the knowledge of Him, which is understanding, will produce but a poor inconsistent character; but duties are enlarged and multiplied by the power and circumstances with which God has intrusted us, and in which He has placed us. Your talents and situation will fit you for public trusts; it is a duty in you to qualify yourself for them, to give your virtue every strength, and then to employ it in the service of your country in its most important interests, true religion, and good government.
  PASSAGE: I hope you will excuse my having said so much, that has the air of advice to one who wants it so little, but young people are apt to be prodigal of time because they think they have so many years before them; but if life be long, the season for improvement is short.
  context after: -

[5] Simon Newcomb, The Reminiscences of an Astronomer (1835–1909)
  context before: I felt its importance at the time. As I walked and walked, the question in my mind was, what am I doing and whither am I going?
  PASSAGE: Am I doing right or wrong? Am I going forward to success in life, or to failure and degradation?
  context after: Vainly, vainly, I tried to peer into the thick darkness of the future. No definite idea of what success might mean could find a place in my mind.

[6] Abraham Lincoln, The Papers and Writings of Abraham Lincoln — Volume 5: 1858-1862 (1809–1865)
  context before: -
  PASSAGE: I fear that the great confidence placed in my ability is unfounded. Indeed, I am sure it is.
  context after: Encompassed by vast difficulties as I am, nothing shall be wanting on my part, if sustained by God and the American people. I believe the devotion to the Constitution is equally great on both sides of the river.

[7] George Sand and Gustave Flaubert, The George Sand-Gustave Flaubert Letters (1804–1876), translated by Aimée L. McKenzie
  context before: I teach my servant to read, I correct proof and I am well. That is my life and nothing bores me in this world where I think that AS FAR AS I AM CONCERNED all is for the best.
  PASSAGE: But I am afraid of becoming more of a bore than I used to be.
  context after: People don't like such as I am very much. We are too inoffensive.

[8] Honoré de Balzac, Letters to Madame Hanska, born Countess Rzewuska, afterwards Madame Honoré de Balzac, 1833-1846 (1799–1850), translated by Katharine Prescott Wormeley
  context before: This letter comes to me at a bad moment. It has singularly added to the dumb grief that gnaws me and will kill me.
  PASSAGE: I am thirty-eight years old, still crippled by debt, with nought but uncertainty as to my position.
  context after: Scarcely have I taken two months to rest my brain before I repent them as a crime when I see the evils that have come through my inaction. This precarious life, which might be a spur in youth, becomes at my age an overwhelming burden.

[9] Adam Gurowski, Diary from November 12, 1862, to October 18, 1863 (1805–1866)
  context before: A critique of the first volume of the "Diary" asserts that all my statements are made after the events occurred, ex post. To a very respectable General I showed a part of the original manuscript which squared with the printed book.
  PASSAGE: Often I am ashamed to find that the bit of study and experience acquired by me goes so far when compared with many around me, and in action.
  context after: I foresee, because I have no earthly personal views, no cares, nothing in the world to think of or to aim at, no charms, no ties--only my heart, my ideas, my convictions, and civilization is my worship. Nothing prevents me, day and night, from concentrating whatever powers and reading I can have in one single focus.

[10] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 2 (1813–1883), translated by Francis Hueffer
  context before: Let me know, in a few words, how things are, and when you are coming. I should certainly like to show you as much as possible of my "Valkyrie," and principally for that reason I did not object to this delay of your much-desired visit.
  PASSAGE: In my present condition, however, I have little hope of gaining much work by this gain of time.
  context after: My mental disharmony is indescribable; sometimes I stare at my paper for days together, without remembrance or thought or liking for my work. Where is that liking to spring from?

[11] Anton Chekhov, Letters to His Family and Friends (1890), translated by Constance Garnett
  context before: It is all the same to me whether I write “The Party” or “The Lights,” or a vaudeville or a letter to a friend--it is all dull, spiritless, mechanical, and I get annoyed with critics who attach any importance to “The Lights,” for instance. I fancy that I deceive him with my work just as I deceive many people with my face, which looks serious or over-cheerful.
  PASSAGE: I don’t like being successful; the subjects which sit in my head are annoyed and jealous of what has already been written.
  context after: I am vexed that the rubbish has been done and the good things lie about in the lumber-room like old books. Of course, in thus lamenting I rather exaggerate, and much of what I say is only my fancy, but there is a part of the truth in it, a good big part of it.

[12] Leo Tolstoy, The Journal of Leo Tolstoi (First Volume—1895-1899) (1828–1910), translated by Rose Strunsky
  context before: To-day November 27. Moscow.
  PASSAGE: Very weak, poor in all respects. And feel as if I had only just now awakened.
  context after: Have been thinking:
1) We are all in this life--workers placed at the work of saving our souls.

[13] John Sherman, Recollections of Forty Years in the House, Senate and Cabinet An Autobiography. (1823–1900)
  context before: "Your suffrages, having elected me to the office of President of the United States, I have, in conformity with the constitution of our country, taken the oath of office prescribed therein. I have taken this oath without mental reservation and with the determination to do to the best of my ability all that it requires of me.
  PASSAGE: The responsibilities of the position I feel but accept them without fear. The office has come to me unsought.
  context after: I commence its duties untrammeled. I bring to it a conscientious desire and determination to fill it to the best of my ability to the satisfaction of the people.

[14] Henry David Thoreau, Journal 01, 1837-1846 The Writings of Henry David Thoreau, Volume 07 (of 20) (1817–1862)
  context before: It is all a mystery to him. "How happens it," he exclaims, "that I find myself making such an enormous demand on men, and so constantly disappointed?
  PASSAGE: Are my friends aware how disappointed I am? Is it all my fault? Am I incapable of expansion and generosity?
  context after: I shall accuse myself of anything else sooner." And again he goes away sorrowful, consoling himself, as best he can, with his own paradox,—

[15] Lafcadio Hearn, Letters from the Raven: Correspondence of L. Hearn with Henry Watkin (1850–1904)
  context before: There were a few exceptions, but these exceptions were cases of extraordinary personal vigor and vital force. So while my whole nature urges me to continue as I have begun, I see nothing in prospect: except starvation, sickness, artificial wants, which I shall never be wealthy enough to even partially gratify, and perhaps utter despair at the end.
  PASSAGE: Then again, while I have not yet lost all confidence in myself, I feel strongly doubtful whether I shall ever have means or leisure to develop the latent (possible) ability within me to do something decently meritorious.
  context after: Perhaps, had I not been constrained to ambition by necessity, I should never have had any such yearnings about the unattainable and iridescent bubbles of literary success. But that has nothing to do with the question.

[16] Elinore Pruitt Stewart, Letters of a Woman Homesteader (1878–?)
  context before: If you only knew how far short I fall of my own hopes you would know I could never boast. Why, it keeps me busy making over mistakes just like some one using old clothes.
  PASSAGE: I get myself all ready to enjoy a success and find that I have to fit a failure.
  context after: But one consolation is that I generally have plenty of material to cut generously, and many of my failures have proved to be real blessings.
I do hope this New Year may bring to you the desire of your heart and all that those who love you best most wish for you.

[17] Charles Darwin, More Letters of Charles Darwin — Volume 2 A Record of His Work in a Series of Hitherto Unpublished Letters (1809–1882)
  context before: You and Bentham must hate the monocotyledons, for what work the Orchideae must have been, and Gramineae and Cyperaceae will be. I am rather despondent about myself, and my troubles are of an exactly opposite nature to yours, for idleness is downright misery to me, as I find here, as I cannot forget my discomfort for an hour.
  PASSAGE: I have not the heart or strength at my age to begin any investigation lasting years, which is the only thing which I enjoy; and I have no little jobs which I can do.
  context after: So I must look forward to Down graveyard as the sweetest place on earth. This place is magnificently beautiful, and I enjoy the scenery, though weary of it; and the weather has been very cold and almost always hazy.

[18] Amy Fay, Music-Study in Germany, from the Home Correspondence of Amy Fay (1844–1928)
  context before: I find that the strengthening and equalizing of the fingers is a terribly slow process, and that it takes much more time to make a step forward than I expected. You may know how a thing ought to be played, but it is another matter to get your hands into such a training that they obey your will.
  PASSAGE: Sometimes I am very much encouraged, and feel as if I should be an artist "immediately, if not sooner," and at others I fall into the blackest despair.
  context after: I don't know but that S. J. was in the right of it, not to attempt anything, for it is an awful pull when you do once begin to study!
I wish S. could come here and spend a winter.

[19] Egerton Ryerson, "The story of my life" (1803–1882)
  context before: I cannot but see that the public mind in this country is in a chaotic state, without any controlling current of feeling, or fixed principle of action, in civil affairs; but susceptible, by proper management and instruction, of being cast into any mould of rational opinion and feeling; yet liable, without judicious direction, to fall into a state of "confusion worse confounded." I know that now is the time--perhaps the only time--to establish our institutions and relations upon the cheapest, the surest, and the only permanent foundation of any system, or form of Government--the sentiments and feelings of the population.
  PASSAGE: But I alone have not the means or the power of contributing to the accomplishment of these objects.
  context after: To the utmost of my humble abilities and acquirements, I am willing to exert myself; and that without a shillings' remuneration--although my present salary is less than L200 per annum. I believe the government about to be established in these provinces may be made the most enduring and loftiest memorial of your Excellency's fame, and the greatest earthly blessing to its inhabitants; and it will be to me a source of satisfaction to contribute towards the formation and cementing of materials for the erection of a monument at once so honourable to its founder, and so beneficial to Her Majesty's Canadian subjects.

[20] James J. Davis, The Iron Puddler: My Life in the Rolling Mills and What Came of It (1873–1947)
  context before: It is four times as strong as yours.” I saw an envious look in his eye.
“Of course I inherited my muscular build,” I apologized, “and so I try to make the most of it in boasting to you fellows who haven't any muscle.
  PASSAGE: But really I envy you. You have education and brain power. That's what I lack and that's what I want above all other things.
  context after: I try to study at night and educate myself. But I haven't got any chance against you fellows who are born intellectual and have college training on top of it.
```

## Case 10: Wound up > rejected

```
(their own words)
  feeling (picked on a feelings wheel): rejected (wound up)
  what's happened: My best friend moved to another city and stopped answering my messages.
  why they think they feel it: I think I did something wrong
  afraid: that I am easy to leave

CANDIDATE PASSAGES
[1] Karl May, My Life and My Efforts (1842–1912), translated by Gunther Olesch
  context before: I was regarded as an intruder, and all of my little, warm needs of a child's soul were offered nothing to satisfy them. I short, I was a stranger to my grade from the start and became more of a stranger with every year.
  PASSAGE: I had lost the class-mates who had fallen behind, without winning those over who were with me.
  context after: Please, do not smile at this seemingly tiny, most insignificant fate of a boy. An educator, knowing his way around in the realm of a person's and a child's soul, will not hesitate for a moment in taking this seriously, very seriously.

[2] Henry David Thoreau, Journal 01, 1837-1846 The Writings of Henry David Thoreau, Volume 07 (of 20) (1817–1862)
  context before: It is all a mystery to him. "How happens it," he exclaims, "that I find myself making such an enormous demand on men, and so constantly disappointed?
  PASSAGE: Are my friends aware how disappointed I am? Is it all my fault? Am I incapable of expansion and generosity?
  context after: I shall accuse myself of anything else sooner." And again he goes away sorrowful, consoling himself, as best he can, with his own paradox,—

[3] Richard Wagner, My Life — Volume 2 (1813–1883)
  context before: As the time for the general leave-taking at last drew near, I had arranged all the details connected with the breaking up of my home. I settled the necessary business part by a personal visit to Herr Wesendonck, and in the presence of Bulow I took leave of Frau Wesendonck, who, in spite of her ever-recurring misconceptions on the matter, eventually reproached herself bitterly when she saw that these misunderstandings had ended by breaking up my home.
  PASSAGE: My friends were much distressed at parting from me, whilst I could only meet their expressions of sorrow with apathy.
  context after: On the 16th August the Bulows also left; Hans was bathed in tears and his wife Cosima was gloomy and silent. I had arranged with Minna that she should remain there for about a week to clear up and dispose of our little belongings as she thought best.

[4] W. H. Davies and Bernard Shaw, The Autobiography of a Super-Tramp (1871–1940)
  context before: It was now the latter end of October, and this pound could not reach London far short of a month. Thinking I was not likely again to suffer for want of a bed or food, after this success in Swindon, I bought a good stock of laces and left that town, with the intention of working the towns on the outskirts of London, so that when ready to enter I would be within a day's march.
  PASSAGE: Unfortunately, after leaving Swindon, success deserted me, which was certainly more my fault than that of the people, for I made very little appeal to them.
  context after: Arriving at Maidenhead, I had the bare price of my bed, with a dry bread supper and breakfast. My laces were being exhausted, and I was without means to replenish them.

[5] Butler, Josephine Elizabeth Grey and James Stuart, Josephine E. Butler: An Autobiographical Memoir (1828–1906)
  context before: * * * * *
After my husband’s serious illness in 1886, I had resolved in my own mind never again to be absent from him for more than a few hours, if possible, during our united lives.
  PASSAGE: I refused all invitations to attend meetings in London or elsewhere, sometimes, I fear, to the surprise as well as the regret of my fellow-workers in public matters.
  context after: My choice was however deliberate, and I have never had cause to regret it. He had, I thought, sufficiently suffered by my frequent absences from home, during many years of our married life, while engaged in opposing a great social wrong, and he had borne this trial without a murmur.

[6] Honoré de Balzac, Letters to Madame Hanska, born Countess Rzewuska, afterwards Madame Honoré de Balzac, 1833-1846 (1799–1850), translated by Katharine Prescott Wormeley
  context before: I spare you the details of the agreement, which has been the object of long examination by my lawyers, and business agents, very devoted men, who think it good and honourable.
You could never believe how I miss the bulletin of your calm and solitary life, what interest I take in that life, and what peace the contemplation of it sheds upon my agitated life.
  PASSAGE: Either it is very bad of you to cut me off, or you are ill; on each side anxiety, thinking that you suffer or that your friendship diminishes.
  context after: Well, adieu. I meant to write you only one word: there is truce between misfortune and me.

[7] Frank Harris, My Life and Loves, Vol. 1 (of 4) (1856–1931)
  context before: I had broken the supreme law of our schoolboy honor: never to give away our dissensions to a master, still less to boys and masters from another school; I had sinned in public, too, and before everyone; I’d be universally condemned.
The truth is, I was desperate, dreadfully unhappy, for since the breakdown of the fags’ revolt the lower boys had drawn away from me and the older boys never spoke to me if they could help it and then it was always as “Pat.”
  PASSAGE: I felt myself an outcast and was utterly lonely and miserable as only despised outcasts can be.
  context after: I was sure, too, I should be expelled and knew my father would judge me harshly; he was always on the side of the authorities and masters. However, the future was not to be as gloomy as my imagination pictured it.

[8] Marion Harland, Marion Harland's Autobiography: The Story of a Long Life (1830–1922)
  context before: Then I opened the Bible and delivered a familiar running lecture upon the lesson for the day. Not a question was asked by one of the dumb eight, and not a comment was made at the close of the “exercises” upon what had been said.
  PASSAGE: I went through the miserable form of shaking hands with them all as we separated, and carried home a thoroughly discouraged spirit.
  context after: By the following Sunday I hit upon the idea of calling upon each student to read a reference text, as it occurred in the course of the lecture, and I took care there should be plenty of them. That was the first crack in the ice.

[9] Sévigné, Marie de Rabutin-Chantal, The letters of Madame de Sévigné (1626–1696)
  context before: At length the ladies arrived in great fear at Paris, where the king, being informed of what had happened, sent a guard to take care of Madame Ventadour, so that she is now under the protection of his majesty. What think you the monster did? he went to the king, attended by his neighbors, that is, the Princes de Condé, de Conti, Messieurs de Luxembourg, Duras, Schomberg, Bellefond; and, with incredible assurance, told the king that the Chevalier de Tilladet had not paid him the respect due to his rank; mark the expression: he places the dukedom where it was formerly. “Sire,” said he, “I want to know why I am refused the company of my wife! what has happened to my person of late?
  PASSAGE: Am I uglier, or more ill made than formerly, when I was as much courted as I am now avoided?
  context after: If I am ugly, sire, is it my fault? Had I been my own maker, I would have been like your majesty; but these are things that are not in our own disposal.” In short, partly owing to this natural and proper, and at the same time unexpected, flattery, and partly to the justice of his argument, the king was pleased with him, as well as the whole court, However, they are to be separated; the difficulty is, that he insists that his wife shall be shut up in a convent, which is a sad affair.

[10] Ambrose Bierce, The Letters of Ambrose Bierce, With a Memoir by George Sterling (1842–1914)
  context before: Thank you so much for the books and the inscription--which (as do all other words of praise) affects me with a sad sense of my shortcomings as writer and man. Things of that kind from too partial friends point out to me with a disquieting significance what I ought to be; and the contrast with what I am hurts.
  PASSAGE: Maybe you feel enough that way sometimes to understand. You are still young enough to profit by the pain; my character is made--my opportunities are gone.
  context after: But it does not greatly matter--nothing does. I have some little testimony from you and Scheff and others that I have not lived altogether in vain, and I know that I have greater satisfaction in my slight connection with your and their work than in my own.

[11] Amy Fay, Music-Study in Germany, from the Home Correspondence of Amy Fay (1844–1928)
  context before: "No; how could I?" said I. "You ought to tell her." So I imagine he did tell her, as they went into supper, that I was the young lady who had described her in the paper.
  PASSAGE: I did not have a chance to approach her again until just as I was going home.
  context after: She was standing in the door-way of an ante-room with Mr. Bancroft, wrapped in her opera cloak and waiting for her carriage to be announced. I bade Mr. Bancroft good-night, and as I passed her she put out her hand and said to me with a meaning look, in her little hesitating English, "I am so happy to have met you."

[12] Felix Moscheles, Fragments of an Autobiography (1833–1917)
  context before: But when I wanted to explain that this my wish was mainly owing to the fact that her hair started in most fascinating wavelets from her temples, there was a kind of barrier that arose to stop me, a halo that came in the way to form a magic circle into which I could not penetrate. I wanted to say something about Helen of Troy, but I did not know what conclusion to draw from her history, and besides it would sound so foolish and priggish.
  PASSAGE: So I said nothing about her, and by the time we got up to return home, I had not done much to improve the opportunity.
  context after: Our skates were once more firmly secured to our feet, and our young ladies comfortably settled in their Stuhlschlitten. We all started together, but soon we broke the ranks, each one taking his own time.

[13] Margaret Sanger, Margaret Sanger: an autobiography. (1879–1966)
  context before: Mr. Untermyer was upset. Instead of his former warmth I was aware of a curt and cold politeness.
  PASSAGE: I went from his office feeling I had had an opportunity to make a powerful friend and had lost it by refusing to accept the legal point of view.
  context after: Max also was decidedly angry. His attitude was, “We tried to help you, and you declined help.” He wrote formally:

[14] James Henry Foss, The gentleman from everywhere (1841–1916)
  context before: I heard a form tumble down the steep stairs, and muffled curses which reminded me of the lines in the Hohenlinden poem: "It is Iser (I sir) rolling rapidly."
At the first dawn of a dismal day I crept down the dirty stairs, and out of the door of what I learned to be one of the most dangerous houses in that sin-cursed city.
  PASSAGE: The days immediately following while seeking for employment were forlorn and miserable; I was the fifth wheel of a coach which no one wanted.
  context after: Finally, when I had spent my last cent for a beggarly meal, I saw an advertisement for a teacher in the reform school, and called on a Mr. Atterbury, the trustee. He regarded me with a pitying eye; told me two teachers had recently been driven from the prison by the kicks and cuffs of the toughest boys that ever went unhung; but if I wished to try it, he would pass me to that "den of thieves."

[15] Georg Brandes, Recollections of My Childhood and Youth (1842–1927)
  context before: Had its recipient known Björnson better, he would in this have found a foundation to build upon. But as things were, I altogether overlooked the honestly meant friendliness in it and merely seized upon the no small portion of it that could not do other than wound.
  PASSAGE: My reply, icy, sharp and in the deeper sense of the word, worthless, was a refusal.
  context after: I did not believe in Björnson, saw in the letter nothing but an attempt to use me as a critic, now that he had lost his former advocate in the Press. The prospect of the journey to the North did not tempt me; in Björnson's eyes it would have been Thor's journey with Loki, and I neither was Loki nor wished to be.

[16] Clifford Whittingham Beers, A Mind That Found Itself: An Autobiography (1876–1943)
  context before: In spite of their unfriendly attitude, however, I did manage to persuade the supervisor, a kindly man, well along in years, to deliver a note to the steward. In it I asked him to come at once, as I wished to talk with him.
  PASSAGE: The steward, whom I looked upon as a friend, returned no answer and made no visit.
  context after: I supposed he, too, had purposely ignored me. As I learned afterwards, both he and the superintendent were absent, else perhaps I should have been treated in a less high-handed manner by the assistant physician, who was not absent.

[17] Helen Keller, The Story of My Life With her letters (1887-1901) and a supplementary account of her education, including passages from the reports and letters of her teacher, Anne Mansfield Sullivan, by John Albert Macy (1880–1968)
  context before: As I wrote you, I meant to go slowly at first. I had an idea that I could win the love and confidence of my little pupil by the same means that I should use if she could see and hear.
  PASSAGE: But I soon found that I was cut off from all the usual approaches to the child's heart.
  context after: She accepted everything I did for her as a matter of course, and refused to be caressed, and there was no way of appealing to her affection or sympathy or childish love of approbation. She would or she wouldn't, and there was an end of it.

[18] George Jacob Holyoake, The History of the Last Trial by Jury for Atheism in England A Fragment of Autobiography Submitted for the Perusal of Her Majesty's Attorney-General and the British Clergy (1817–1906)
  context before: I answered, 'I think you have mistaken me. The opinions I defended are also my convictions; and thinking them useful, it seems my duty to propagate them, and the discharge of this duty is more serious in my eyes than you suppose; nor do the inducements you picture exist.
  PASSAGE: Do you not see that I am nearly friendless? I am without even the attentions of those from whom I have some right to expect it.
  context after: Except Mr. Farn, Mr. Watts, and Mr. Campbell, none of my colleagues among the Social Missionaries have written me a friendly word. The editor of the New Moral World, upon whose protection I have some claim, has written no word in my favour.

[19] Mary Casal, The stone wall (1864–1935)
  context before: What he said to them I never knew, but I was informed by those good people that it was their desire, for reasons which they chose to keep to themselves, that my friendship with their daughter should cease.
My school had grown to such proportions that I had now taken a large studio apartment on Washington Square.
  PASSAGE: This girl came to me one day in despair, and told me that she had been forbidden my friendship.
  context after: She was in a state of rebellion, as she had no idea of what was back of it all. She said it was so unfair that she would not obey them, and she would come to me, as she was so fond of me she could not give our friendship up.

[20] Benito Mussolini and Richard Washburn Child, My autobiography (1883–1945)
  context before: His body was carried to the churchyard of Forli. I had gone to Forli for a rest, with some political friends.
  PASSAGE: My reception in my own home district had been cold and even hostile. My efforts to be agreeable and my willingness to learn to fly just after Ridolfi had lost his life seemed to be quite wasted.
  context after: Anything in those days that did not have a material value seemed to be superfluous. Those were years when men’s hearts were gray.
```
