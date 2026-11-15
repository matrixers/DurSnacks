# Judge input (step1)

You are matching a person's problem to passages from real historical letters and diaries.

Goal: find a passage where the WRITER is facing the same underlying problem as the person:
the same kind of situation, felt for the same kind of reason, with the same fear about what it means.
Sharing a topic or words is NOT enough (a passage about letters is not a match for "nobody replies to me"
unless the writer is the one waiting and hurt). A writer describing someone else's problem, giving advice,
or saying they are NOT troubled is not a match.

Judge only from the text given. Do not guess what the writer felt if the text does not show it.
"none" is a correct answer when no passage is a real match.

For each candidate give:
  situation: yes | partly | no      (same kind of thing happening to the writer)
  cause:     yes | partly | no | not stated   (same kind of reason for the feeling)
  fear:      yes | partly | no | not stated   (same fear about what it means)
  overall:   yes | partly | no
  why:       one short sentence
Then give "best": the number of the single best candidate whose overall is yes or partly, or "none".
Reply with JSON only, in exactly this format:

```json
{
 "verdicts": [
  {
   "n": 1,
   "situation": "yes",
   "cause": "partly",
   "fear": "not stated",
   "overall": "partly",
   "why": "..."
  }
 ],
 "best": 1
}
```

## Case 1: Sad > Lonely > Isolated

```
feeling: isolated (lonely, sad)
  what happened: Nobody has replied to my messages in weeks.
  because: my friends seem to have forgotten me
  afraid it means: that I am easy to forget

CANDIDATE PASSAGES
[1] John Adams and Abigail Adams, Familiar Letters of John Adams and His Wife Abigail Adams During the Revolution with a Memoir of Mrs. Adams (1735–1826)
  context before: Next Wednesday is thirteen weeks since you went away. I must bid you adieu.
  PASSAGE: You have many friends, though they have not noticed you by writing. I am sorry they have been so negligent. I hope no share of that blame lies upon
  context after: -

[2] Arthur Christopher Benson, The Upton Letters (1862–1925)
  context before: But I am here, a lonely man, wondering and doubting and desiring I hardly know what. Some nearness of life, some children of my own.
  PASSAGE: You are apt to think of yourself as shelved and isolated; yet, after all, you have the real thing--wife, children, and home. But, in my case, these boys who are dear to me have forgotten me already.
  context after: Disguise it as I will, I am part of the sordid furniture of life that they have so gladly left behind, the crowded corridor, the bare-walled schoolroom, the ink-stained desk. They are glad to think that they have not to assemble to-morrow to listen to my prosing, to bear the blows of the uncle's tongue, as Horace says.

[3] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 1 (1813–1883)
  context before: I can get no real information from there. It is very long since I heard anything of you!
  PASSAGE: Alas! I am out of sorts and God-forsaken. I feel so lonely, and yet do not want to see any one. What a miserable existence!
  context after: I cannot help smiling when I read in B.'s paper the articles by R. F.'s brother-in-law; the man thinks he is going thoroughly to the bottom of the thing, because he is so moderate and cautious; he knows very little of me.

[4] Samuel Taylor Coleridge, Biographia Epistolaris, Volume 1 (1772–1834)
  context before: -
  PASSAGE: You are very right, I have neglected my absent friends, but do not think I have forgot them, and indeed it would be ungrateful in me if I did not write to them.
  context after: You may be sure, Nancy, I thank Providence for bringing about that meeting, which has been the cause of all my good fortune and happiness, which I now in fulness enjoy. It was an affectionate meeting, and I will inform you of the particulars.

[5] George Sand and Gustave Flaubert, The George Sand-Gustave Flaubert Letters (1804–1876)
  context before: It is warm, I am alive, I am calm and sad, I hardly know why. In this existence so even, so tranquil, and so gentle as I have here, I am in an element that weakens me morally while strengthening me physically; and I fall into melancholies of honey and roses which are none the less melancholy.
  PASSAGE: It seems to me that all those I love forget me, and that it is justice, because I live a selfish life having nothing to do for any one of them.
  context after: I have lived with tremendous attachments which overwhelmed me, which exceeded my strength and which I often used to curse. And it happens that having nothing more to carry them on with, I am bored by being well.

[6] Horace Walpole, The Letters of Horace Walpole, Earl of Orford — Volume 1 (1717–1797)
  context before: I have always flung it away all in the most idle manner; but, my dear Harry, idle -,is I am, and thoughtless, I have sense enough to have real pleasure in denying myself baubles, and in saving a very good income to make a man happy, for whom I have a just esteem and most sincere friendship. I know the difficulties any gentleman and man of spirit must struggle with, even in having such an offer made him, much more in accepting it.
  PASSAGE: I hope you will allow there are some in making it. But hear me: if there is such a thing as friendship in the world, these are the opportunities of exerting it, and it can't be exerted without it is accepted.
  context after: I must talk of myself to prove to you that it will be right for 'you to accept it. I am sensible of having more follies and weaknesses, and fewer real good qualities than most men.

[7] Charles Lever, Charles Lever, His Life in His Letters, Vol. II (1806–1872)
  context before: “A Mr Crane, West George Street, Glasgow, writes me a very courteous note, and says, ‘I do thank the Editor of “Blackwood” for publishing what you say of Scott,’ and goes on to express his hearty concurrence with it all, and he regrets that it had not been spoken instead of written, &c, &c.
“I do not feel as if I was to get better this time; but I have called wolf so often I shall scream no more.
  PASSAGE: What I feel most, and struggle against most in vain, is depression. I have got to believe not only that my brains are leaving me, but that my friends are tired of me.
  context after: Of course, I couple the two disasters together, and long to be beyond the reach of remembering either one or the other.
“You read my MS. so easily that if you do not like the O’D. don’t print it--it saves me a disappointment at least; and above all, do not mind any chance irritability I display in writing, for a cry escapes me in my pain, and I often do not hear it myself.

[8] Charles Lamb and Mary Lamb, The Works of Charles and Mary Lamb — Volume 6 Letters 1821-1842 (1775–1834)
  context before: I have a glimpse of Freedom, of becoming a Gentleman at large, but I am put off from day to day. I have offered my resignation, and it is neither accepted nor rejected.
  PASSAGE: Eight weeks am I kept in this fearful suspence. Guess what an absorbing stake I feel it. I am not conscious of the existence of friends present or absent.
  context after: The E.I. Directors alone can be that thing to me--or not.--

[9] Walter Scott, The Journal of Sir Walter Scott From the Original Manuscript at Abbotsford (1771–1832)
  context before: February 12.--Having ended the second volume of Woodstock last night, I have to begin the third this morning. Now I have not the slightest idea how the story is to be wound up to a catastrophe.
  PASSAGE: I am just in the same case as I used to be when I lost myself in former days in some country to which I was a stranger.
  context after: I always pushed for the pleasantest road, and either found or made it the nearest. It is the same in writing, I never could lay down a plan--or, having laid it down, I never could adhere to it; the action of composition always diluted some passages, and abridged or omitted others; and personages were rendered important or insignificant, not according to their agency in the original conception of the plan, but according to the success, or otherwise, with which I was able to bring them out.

[10] Napoleon I, Emperor of the French, Napoleon's Letters to Josephine, 1796-1812 For the First Time Collected and Translated, with Notes Social, Historical, and Chronological, from Contemporary Sources (1769–1821)
  context before: Every day I wait impatiently for the post which will bring me news of you--you are well aware how I prize it. Far from you I cannot live, the happiness of my life is near my gentle Josephine.
  PASSAGE: Think of me! Write me often, very often: in absence it is the only remedy: it is cruel, but, I hope, will be only temporary.
  context after: -

[11] Charles Lamb, The Best Letters of Charles Lamb (1775–1834)
  context before: Eight weeks am I kept in this fearful suspense. Guess what an absorbing state I feel it.
  PASSAGE: I am not conscious of the existence of friends, present or absent. The East India directors alone can be that thing to me. I have just learned that nothing will be decided this week.
  context after: Why the next? Why any week?"

[12] Byron, George Gordon Byron, The Works of Lord Byron: Letters and Journals. Vol. 2 (1788–1824)
  context before: -
  PASSAGE: I am too proud of being your friend, to care with whom I am linked in your estimation, and, God knows, I want friends more at this time than at any other.
  context after: I am "taking care of myself" to no great purpose. If you knew my situation in every point of view, you would excuse apparent and unintentional neglect.

[13] Robert E. Lee, Recollections and Letters of General Robert E. Lee (1843–1914)
  context before: I think you had better also begin to make arrangements to build yourself a house. If you can do nothing more than prepare a site, lay out a garden, orchard, etc., and get a small house partly finished, so as to inhabit it, it will add to your comfort and health.
  PASSAGE: I can help you in that too. Think about it. Then, too, you must get a nice wife. I do not like you being so lonely.
  context after: I fear you will fall in love with celibacy. I have heard some very pleasing reports of Fitzhugh.

[14] William Hazlitt, Liber Amoris, Or, The New Pygmalion (1778–1830)
  context before: The agony, the conflict of hope and fear, of adoration and jealousy is over; or it would, ere long, have ended with my life. I am no more lifted now to Heaven, and then plunged in the abyss; but I seem to have been thrown from the top of a precipice, and to lie groveling, stunned, and stupefied.
  PASSAGE: I am melancholy, lonesome, and weaker than a child. The worst is, I have no prospect of any alteration for the better: she has cut off all possibility of a reconcilement at any future period.
  context after: Were she even to return to her former pretended fondness and endearments, I could have no pleasure, no confidence in them. I can scarce make out the contradiction to myself.

[15] Roe, Frances Marie Antoinette Mack, Army Letters from an Officer's Wife, 1871-1888 (?–1920)
  context before: Major Pierce was promoted to another regiment and we miss them very much.
FORT SHAW, MONTANA TERRITORY, July, 1882.
  PASSAGE: THE garrison seems lonesome since the two companies have been out, and I am beginning to feel that I am at home alone quite too much.
  context after: Faye was in Washington two months, and almost immediately after he got back he was ordered to command the paymaster's escort from Helena here, and now he is off again for the summer! The camp is on Birch Creek not far from the Piegan Agency.

[16] Ambrose Bierce, The Letters of Ambrose Bierce, With a Memoir by George Sterling (1842–1914)
  context before: I hope to do a little, now and then, to further your success in letters. I wish you were different (and that is the harshest criticism that I ever uttered of you except to yourself) and wish it for your sake more than for mine.
  PASSAGE: I am older than you and probably more "acquainted with grief"--the grief of disappointment and disillusion. If in the future you are convinced that you have become different, and I am still living, my welcoming hand awaits you.
  context after: And when I forgive I forgive all over, even the new offence.
Miller undoubtedly is sincere in his praise of you, for with all his faults and follies he is always generous and usually over generous to other poets.

[17] Andrew Everett Durham, Epistles from Pap: Letters from the man known as 'The Will Rogers of Indiana' (1882–1954)
  context before: My head is swollen to double, my sight in one eye may be gone. I still bleed at the nose. . .My mental anguish is unbearable.
  PASSAGE: I know that which I had in abundance and have ample living proof of is gone from me, never to return. I have lost my social standing in the community in which I reside and my wimmen folks are laughing at me and at this time of the year. . .
  context after: Oh, grave, where is thy sting. . .
If you care to apologize for your hasty remarks about bull mental pain and anguish, you may address me as: Respectfully, The Bull

[18] Mark Twain, Mark Twain's Letters — Volume 4 (1886-1900) (1835–1910)
  context before: ROGERS,--Notwithstanding your heart is “old and hard,” you make a body choke up. I know you “mean every word you say” and I do take it “in the same spirit in which you tender it.” I shall keep your regard while we two live--that I know; for I shall always remember what you have done for me, and that will insure me against ever doing anything that could forfeit it or impair it.
  PASSAGE: I am 59 years old; yet I never had a friend before who put out a hand and tried to pull me ashore when he found me in deep waters.
  context after: It is six days or seven days ago that I lived through that despairing day, and then through a night without sleep; then settled down next day into my right mind (or thereabouts,) and wrote you. I put in the rest of that day till 7 P.

[19] Thomas Carlyle and Ralph Waldo Emerson, The Correspondence of Thomas Carlyle and Ralph Waldo Emerson, 1834-1872, Vol. I (1795–1881)
  context before: Surely, I often say, if ever man had a finger-of-Providence shown him, thou hast it; literature will neither yield thee bread, nor a stomach to digest bread with: quit it in God's name, shouldst thou take spade and mattock instead. The truth is, I believe literature to be as good as dead and gone in all parts of Europe at this moment, and nothing but hungry Revolt and Radicalism appointed us for perhaps three generations; I do not see how a man can honestly live by writing in another dialect than that, in England at least; so that if you determine on not living dishonestly, it will behove you to look several things full in the face, and ascertain what is what with some distinctness.
  PASSAGE: I suffer also terribly from the solitary existence I have all along had; it is becoming a kind of passion with me, to feel myself among my brothers.
  context after: And then, How? Alas!

[20] Dorothy Osborne, The Love Letters of Dorothy Osborne to Sir William Temple, 1652-54 (1627–1695)
  context before: I shall not be so unreasonable as to desire that, for my satisfaction, you should deny yourself a recreation that is pleasing to you, and very innocent, sure, when 'tis not used in excess, but I cannot consent you should disorder yourself with it, and Jane was certainly in the right when she told you I would have chid if I had seen you so endanger a health that I am so much concerned in. But for what she tell you of my melancholy you must not believe; she thinks nobody in good humour unless they laugh perpetually, as Nan and she does, which I was never given to much, and now I have been so long accustomed to my own natural dull humour that nothing can alter it.
  PASSAGE: 'Tis not that I am sad (for as long as you and the rest of my friends are well), I thank God I have no occasion to be so, but I never appear to be very merry, and if I had all that I could wish for in the world, I do not think it would make any visible change in my humour.
  context after: And yet with all my gravity I could not but laugh at your encounter in the Park, though I was not pleased that you should leave a fair lady and go lie upon the cold ground. That is full as bad as overheating yourself at tennis, and therefore remember 'tis one of the things you are forbidden.
```

## Case 2: Scared > Submissive > Inadequate

```
feeling: inadequate (submissive, scared)
  what happened: I failed my exams and everyone on my course did better than me.
  because: I am not clever enough for this course
  afraid it means: that I will never make anything of myself

CANDIDATE PASSAGES
[1] Mark Twain, Mark Twain's Letters — Volume 5 (1901-1906) (1835–1910)
  context before: But there is the tempermental difference. You are dramatic and unconscious; you count the thing more than yourself; I am cursed with consciousness to the core, and can't say myself out; I am always saying myself in, and setting myself above all that I say, as of more worth.
  PASSAGE: Lately I have felt as if I were rotting with egotism. I don't admire myself; I am sick of myself; but I can't think of anything else.
  context after: Here I am at it now, when I ought to be rejoicing with you at the blessing you have found.... I'd like, immensely, to read your autobiography.

[2] Adam Gurowski, Diary from November 12, 1862, to October 18, 1863 (1805–1866)
  context before: A critique of the first volume of the "Diary" asserts that all my statements are made after the events occurred, ex post. To a very respectable General I showed a part of the original manuscript which squared with the printed book.
  PASSAGE: Often I am ashamed to find that the bit of study and experience acquired by me goes so far when compared with many around me, and in action.
  context after: I foresee, because I have no earthly personal views, no cares, nothing in the world to think of or to aim at, no charms, no ties--only my heart, my ideas, my convictions, and civilization is my worship. Nothing prevents me, day and night, from concentrating whatever powers and reading I can have in one single focus.

[3] Fanny Burney, The Diary and Letters of Madame D'Arblay — Volume 3 (1752–1840)
  context before: Dr. Elloi now came not only every day, but almost every hour of the day, to obtain another interview; but my beloved, though pleased that the meeting had taken place, expressed no desire for its repetition.
  PASSAGE: I was cruelly distressed ; the fear of doing wrong has been always the leading principle of my internal guidance, and here I felt incompetent to judge what was right.
  context after: Overpowered, therefore, by my own inability to settle that point, and my terror lest I should mistake it, I ceased to resist ; and Dr. Elloi, while my patient was sleeping from opium, glided into his chamber, and knelt down by the bedside with his prayer book in his hand.

[4] Nathaniel Hawthorne, Passages from the English Notebooks, Volume 1. (1804–1864)
  context before: My early life was perhaps a good preparation for the declining half of life; it having been such a blank that any thereafter would compare favorably with it. For a long, long while, I have occasionally been visited with a singular dream; and I have an impression that I have dreamed it ever since I have been in England.
  PASSAGE: It is, that I am still at college,--or, sometimes, even at school,--and there is a sense that I have been there unconscionably long, and have quite failed to make such progress as my contemporaries have done; and I seem to meet some of them with a feeling of shame and depression that broods over me as I think of it, even when awake.
  context after: This dream, recurring all through these twenty or thirty years, must be one of the effects of that heavy seclusion in which I shut myself up for twelve years after leaving college, when everybody moved onward, and left me behind. How strange that it should come now, when I may call myself famous and prosperous!--when I am happy, too!

[5] George Sand and Gustave Flaubert, The George Sand-Gustave Flaubert Letters (1804–1876)
  context before: CCXCVI. TO GUSTAVE FLAUBERT, at Croissset Nohant, 7th September, 1875
  PASSAGE: You are distressed, you are discouraged, you distress me too. That is all right, I would rather have you complain than keep silent, dear friend.
  context after: And I don't want you to stop writing to me.
I also have great and frequent sorrows.

[6] Charles Lamb and Mary Lamb, The Works of Charles and Mary Lamb — Volume 5 The Letters of Charles and Mary Lamb, 1796-1820 (1775–1834)
  context before: Your kind heart will, I know, even if you have been a little displeased, forgive me, when I assure you my spirits have been so much hurt by my last illness, that at times I hardly know what I do. I do not mean to alarm you about myself, or to plead an excuse; but I am very much otherwise than you have always known me.
  PASSAGE: I do not think any one perceives me altered, but I have lost all self-confidence in my own actions, and one cause of my low spirits is, that I never feel satisfied with any thing I do--a perception of not being in a sane state perpetually haunts me.
  context after: I am ashamed to confess this weakness to you; which, as I am so sensible of, I ought to strive to conquer. But I tell you, that you may excuse any part of my letter that has given offence: for your not answering it, when you are such a punctual correspondent, has made me very uneasy.

[7] Charles Darwin, Life and Letters of Charles Darwin — Volume 2 (1809–1882)
  context before: Soc., but by Jove the Linn. Soc. produced a tremendous effect on me, for I could not get out of bed till late next evening, so that I just crawled home.
  PASSAGE: I fear I must give up trying to read any paper or speak; it is a horrid bore, I can do nothing like other people."
  context after: To Dr. Gray he wrote, (December 1861):--

[8] Henri Frédéric Amiel, Amiel's Journal: The Journal Intime of Henri-Frédéric Amiel (1821–1881)
  context before: (Hyères.)--In spite of my sleeping draught I have had a bad night. Once it seemed as if I must choke, for I could breathe neither way.
  PASSAGE: Could I be more fragile, more sensitive, more vulnerable! People talk to me as if there were still a career before me, while all the time I know that the ground is slipping from under me, and that the defense of my health is already a hopeless task.
  context after: At bottom, I am only living on out of complaisance and without a shadow of self-delusion. I know that not one of my desires will be realized, and for a long time I have had no desires at all.

[9] Theodore Roosevelt, Letters to His Children (1858–1919)
  context before: -
  PASSAGE: I puzzled a good deal over your marks. I am inclined to think that one explanation is that you have thought so much of home as to prevent your really putting your whole strength into your studies.
  context after: It is most natural that you should count the days before coming home, and write as you do that it will only be 33 days, only 26 days, only 19 days, etc., but at the same time it seems to me that perhaps this means that you do not really put all your heart and all your head effort into your work; and that if you are able to, it would be far better to think just as little as possible about coming home and resolutely set yourself to putting your best thought into your work. It is an illustration of the old adage about putting your hand to the plow and then looking back.

[10] Fanny Kemble, Records of Later Life (1809–1893)
  context before: ... God knows I am admonished to patience, both by my own helplessness and the inefficiency of those who, it seems to me, ought to be able to help me....
  PASSAGE: Doubtless, my father reasonably regrets the independence which I might by this time have earned for myself in my profession, and feels anxious about my unprovided future.
  context after: I have written to Chorley, the only person I know to whom I can apply on the subject, to get me some means of publishing the few manuscript verses I have left in some magazine or other.... If I cannot succeed in this, I shall try if I can publish my "English Tragedy," and make a few pounds by it.

[11] Charles Dickens, The Letters of Charles Dickens. Vol. 2, 1857-1870 (1812–1870)
  context before: It is simply to say what follows, which I hope may save you some mental uneasiness. For I was stricken ill when I was doing "Bleak House," and I shall not easily forget what I suffered under the fear of not being able to come up to time.
  PASSAGE: Dismiss that fear (if you have it) altogether from your mind. Write to me at Paris at any moment, and say you are unequal to your work, and want me, and I will come to London straight and do your work.
  context after: I am quite confident that, with your notes and a few words of explanation, I could take it up at any time and do it. Absurdly unnecessary to say that it would be a makeshift!

[12] Arthur Christopher Benson, The Upton Letters (1862–1925)
  context before: Well, then, a few days ago I woke early, after troubled dreams, and knew that the old enemy had clutched me. I lay in a strange agony of mind, my heart beating thick, and with an insupportable weight on my heart.
  PASSAGE: It always takes the same form with me--an overwhelming sense of failure in all that I attempt, a dreary consciousness of absolute futility, coupled with the sense of the brevity and misery of human life generally.
  context after: I ask myself what is the use of anything? What is an almost demoniacal feature of the mood is that it lays a spell of utter dreariness upon all pleasures as well as duties.

[13] Horace Walpole, The Letters of Horace Walpole, Earl of Orford — Volume 4 (1717–1797)
  context before: I wish, in No. 20, you had not again named October or November. I have quite given up those months, and am vexed I ever pressed for them, as they would break into Your reasonable plans, for which I abandon any foolish ones of my own.
  PASSAGE: But I am a poor philosopher, or rather am like all philosophers, have no presence of mind, and must study my part before I can act it.
  context after: I have now settled myself not to expect you this year-do not unsettle me: I dread a disappointment, as I do a relapse of the gout; and therefore cut this article short, that I may not indulge vain hopes, My affection for you both is unalterable; can I give so strong a proof as by supplicating you, as I do earnestly, to act as is most prudent for your healths and interest? A long journey in November would be the very worst part you could take. and I beseech you not to think of it: for me, you see I take a great deal of killing, nor is it so easy to die as is imagined.

[14] Edward FitzGerald, Letters of Edward FitzGerald, in Two Volumes. Vol. 1 (1809–1883)
  context before: So indeed it is so far easy to write down one's two ideas, if they are not very abstruse ones; but then what the devil encouragement is it to a poor fellow to expose his nakedness so? All I can say is, to say again that if you lived in this place, you would not write so long a letter as you have done, full of capital description and all good things; though without any compliment I am sure you would write a better than I shall.
  PASSAGE: But you see the original fault in me is that I choose to be in such a place as this at all; that argues certainly a talent for dullness which no situation nor intercourse of men could much improve.
  context after: It is true; I really do like to sit in this doleful place with a good fire, a cat and dog on the rug, and an old woman in the kitchen. This is all my live stock.

[15] Robert Louis Stevenson, The Letters of Robert Louis Stevenson — Volume 2 (1850–1894)
  context before: I pulled it off, of course, I won the wager, and it is pleasant while it lasts; but how long will it last? I don’t know, say the Bells of Old Bow.
  PASSAGE: All of which goes to show that nobody is quite sane in judging himself. Truly, had I given way and gone in for engineering, I should be dead by now.
  context after: Well, the gods know best.
. . .

[16] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 1 (1813–1883)
  context before: Or shall I look on indifferently, amuse myself when I can make a hundred thalers, buy champagne, and turn my back upon the world? It is a misery.
  PASSAGE: I am going from bad to worse every day, and lead an indescribably worthless life. Of real enjoyment of life I know nothing; to me "enjoyment of life, of love," is a matter of imagination, not of experience.
  context after: In this manner my heart has to go to my brain, and my life becomes an artificial one; only as an "artist" I can live; in the artist my whole "man" has been sunk.
If I could visit you in Weimar and see a performance of my operas now and then, I might perhaps still hope to recover.

[17] Robert Browning and Elizabeth Barrett Browning, The letters of Robert Browning and Elizabeth Barrett Barrett, Vol. 1 (of 2) 1845-1846 (1812–1889)
  context before: -
  PASSAGE: I had begun to be afraid that I did not deserve to have my questions answered; and I was afraid of asking them over again.
  context after: But it is worse to be afraid that you are not better at all in any essential manner (after all your assurances) and that the medical means have failed so far. Did you go to somebody who knows anything?--because there is no excuse, you see, in common sense, for not having the best and most experienced opinion when there is a choice of advice--and I am confident that that pain should not be suffered to go on without something being done.

[18] Charles Lever, Charles Lever, His Life in His Letters, Vol. II (1806–1872)
  context before: “A Mr Crane, West George Street, Glasgow, writes me a very courteous note, and says, ‘I do thank the Editor of “Blackwood” for publishing what you say of Scott,’ and goes on to express his hearty concurrence with it all, and he regrets that it had not been spoken instead of written, &c, &c.
“I do not feel as if I was to get better this time; but I have called wolf so often I shall scream no more.
  PASSAGE: What I feel most, and struggle against most in vain, is depression. I have got to believe not only that my brains are leaving me, but that my friends are tired of me.
  context after: Of course, I couple the two disasters together, and long to be beyond the reach of remembering either one or the other.
“You read my MS. so easily that if you do not like the O’D. don’t print it--it saves me a disappointment at least; and above all, do not mind any chance irritability I display in writing, for a cry escapes me in my pain, and I often do not hear it myself.

[19] John Adams and Abigail Adams, Familiar Letters of John Adams and His Wife Abigail Adams During the Revolution with a Memoir of Mrs. Adams (1735–1826)
  context before: My friends assure me from their observations that you must have had a good passage. God grant it, I say, but my fears and anxieties are many, very many.
  PASSAGE: I had a faith and reliance that supported me before, but now my heart so misgives me that I cannot find that confidence which I wish for.
  context after: Your letter from Cape Ann arrived and cheered my drooping spirits. Could I hear of your safe arrival, I would try to compose my agitated mind, which has horrors both day and night.

[20] John Ruskin, Hortus Inclusus Messages from the Wood to the Garden, Sent in Happy Days to the Sister Ladies of the Thwaite, Coniston (1819–1900)
  context before: I have done it to rocks often, seldom to flowers, not being sure that they would like it.
I recollect giving a very reverent little kiss to a young sapling that was behaving beautifully in an awkward chink, between two great big ones that were ill-treating it.
  PASSAGE: Poor me, (I'm old enough, I hope, to write grammar my own way,) my own little self, meantime, never by any chance got a kiss when I wanted it,--and the better I behaved, the less chance I had, it seemed.
  context after: * * * * *
I never thought the large packet was from you; it was thrown aside with the rest, till evening, and only opened then by chance.
```

## Case 3: Sad > Depressed > Inferior

```
feeling: inferior (depressed, sad)
  what happened: My dad died this year.
  because: I miss him and I do not know how to carry on without him
  afraid it means: that the best part of my life is over

CANDIDATE PASSAGES
[1] Forbes Robinson, Letters to His Friends (1867–1904)
  context before: -
  PASSAGE: . . . I do feel for you, and could do a great deal to help you. I can only tell you what I have felt to be the only thing which makes life endurable at a time of real sorrow--God Himself.
  context after: He comes unutterably near in trouble. In fact, one scarcely knows He exists until one loves or sorrows.

[2] Charles Lever, Charles Lever, His Life in His Letters, Vol. II (1806–1872)
  context before: “A Mr Crane, West George Street, Glasgow, writes me a very courteous note, and says, ‘I do thank the Editor of “Blackwood” for publishing what you say of Scott,’ and goes on to express his hearty concurrence with it all, and he regrets that it had not been spoken instead of written, &c, &c.
“I do not feel as if I was to get better this time; but I have called wolf so often I shall scream no more.
  PASSAGE: What I feel most, and struggle against most in vain, is depression. I have got to believe not only that my brains are leaving me, but that my friends are tired of me.
  context after: Of course, I couple the two disasters together, and long to be beyond the reach of remembering either one or the other.
“You read my MS. so easily that if you do not like the O’D. don’t print it--it saves me a disappointment at least; and above all, do not mind any chance irritability I display in writing, for a cry escapes me in my pain, and I often do not hear it myself.

[3] Henri Frédéric Amiel, Amiel's Journal: The Journal Intime of Henri-Frédéric Amiel (1821–1881)
  context before: -
  PASSAGE: Do I feel any relief, any joy, pride, hope? Hardly. It seems to me that I feel nothing at all, or at least my feeling is so vague and doubtful that I cannot analyze it.
  context after: On the whole, I am rather tempted to say to myself, how much labor for how small a result--Much ado about nothing! And yet the work in itself is good, is successful.

[4] Ambrose Bierce, The Letters of Ambrose Bierce, With a Memoir by George Sterling (1842–1914)
  context before: Thank you so much for the books and the inscription--which (as do all other words of praise) affects me with a sad sense of my shortcomings as writer and man. Things of that kind from too partial friends point out to me with a disquieting significance what I ought to be; and the contrast with what I am hurts.
  PASSAGE: Maybe you feel enough that way sometimes to understand. You are still young enough to profit by the pain; my character is made--my opportunities are gone.
  context after: But it does not greatly matter--nothing does. I have some little testimony from you and Scheff and others that I have not lived altogether in vain, and I know that I have greater satisfaction in my slight connection with your and their work than in my own.

[5] Andrew Everett Durham, Epistles from Pap: Letters from the man known as 'The Will Rogers of Indiana' (1882–1954)
  context before: My head is swollen to double, my sight in one eye may be gone. I still bleed at the nose. . .My mental anguish is unbearable.
  PASSAGE: I know that which I had in abundance and have ample living proof of is gone from me, never to return. I have lost my social standing in the community in which I reside and my wimmen folks are laughing at me and at this time of the year. . .
  context after: Oh, grave, where is thy sting. . .
If you care to apologize for your hasty remarks about bull mental pain and anguish, you may address me as: Respectfully, The Bull

[6] Mark Twain, Mark Twain's Letters — Volume 5 (1901-1906) (1835–1910)
  context before: But there is the tempermental difference. You are dramatic and unconscious; you count the thing more than yourself; I am cursed with consciousness to the core, and can't say myself out; I am always saying myself in, and setting myself above all that I say, as of more worth.
  PASSAGE: Lately I have felt as if I were rotting with egotism. I don't admire myself; I am sick of myself; but I can't think of anything else.
  context after: Here I am at it now, when I ought to be rejoicing with you at the blessing you have found.... I'd like, immensely, to read your autobiography.

[7] George Sand and Gustave Flaubert, The George Sand-Gustave Flaubert Letters (1804–1876)
  context before: I don't know one of them who would be capable of passing an afternoon with me reading a poet. They have their business; I, I have none.
  PASSAGE: Observe that I am in the same social position that I was at eighteen. My niece whom I love as my daughter, does not live with me, and my poor good simple mother has become so old that all conversation with her (except about her health) is impossible.
  context after: All that makes an existence which is not diverting.
As for the ladies, "my little locality" furnishes none of them, and then,--even so!

[8] Robert Browning and Elizabeth Barrett Browning, The letters of Robert Browning and Elizabeth Barrett Barrett, Vol. 1 (of 2) 1845-1846 (1812–1889)
  context before: Or one verse will do ... anything will do ... and don't let me be bringing you into vexation. It need not be of MS. rarity.
  PASSAGE: You are not better ... really ... I fear. And your mother's being ill affects you more than you like to admit, I fear besides.
  context after: Will you, when you write, say how both are ... nothing extenuating, you know. May God bless you, my dearest friend.

[9] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 1 (1813–1883)
  context before: Or shall I look on indifferently, amuse myself when I can make a hundred thalers, buy champagne, and turn my back upon the world? It is a misery.
  PASSAGE: I am going from bad to worse every day, and lead an indescribably worthless life. Of real enjoyment of life I know nothing; to me "enjoyment of life, of love," is a matter of imagination, not of experience.
  context after: In this manner my heart has to go to my brain, and my life becomes an artificial one; only as an "artist" I can live; in the artist my whole "man" has been sunk.
If I could visit you in Weimar and see a performance of my operas now and then, I might perhaps still hope to recover.

[10] Fanny Kemble, Journal of a Residence on a Georgian Plantation: 1838-1839 (1809–1893)
  context before: Friday, March 1.--Last night after writing so much to you I felt weary, and went out into the air to refresh my spirit. The scene just beyond the house was beautiful, the moonlight slept on the broad river which here is almost the sea, and on the masses of foliage of the great southern oaks; the golden stars of German poetry shone in the purple curtains of the night, and the measured rush of the Atlantic unfurling its huge skirts upon the white sands of the beach (the sweetest and most awful lullaby in nature) resounded through the silent air.
  PASSAGE: I have not felt well, and have been much depressed for some days past. I think I should die if I had to live here.
  context after: This morning, in order not to die yet, I thought I had better take a ride, and accordingly mounted the horse which I told you was one of the equestrian alternatives offered me here; but no sooner did he feel my weight, which, after all, is mere levity and frivolity to him, than he thought proper to rebel, and find the grasshopper a burthen, and rear and otherwise demonstrate his disgust. I have not ridden for a long time now, but Montreal's opposition very presently aroused the Amazon which is both natural and acquired in me, and I made him comprehend that, though I object to slaves, I expect obedient servants; which views of mine being imparted by a due administration of both spur and whip, attended with a judicious combination of coaxing pats on his great crested neck, and endearing commendations of his beauty, produced the desired effect.

[11] John Keats, Letters to His Family and Friends (1819)
  context before: The reason of my delaying is oftentimes from this feeling,--I wait for a proper temper. Now you ask for an immediate answer, I do not like to wait even till to-morrow.
  PASSAGE: However, I am now so depressed that I have not an idea to put to paper--my hand feels like lead--and yet it is an unpleasant numbness; it does not take away the pain of Existence.
  context after: I don't know what to write.

[12] Arthur Christopher Benson, The Upton Letters (1862–1925)
  context before: UPTON, Dec. 5, 1904.
  PASSAGE: MY DEAR HERBERT,--I am very sorry to hear you have been suffering from depression; it is one of the worst evils of life, and none the better for being so intangible.
  context after: I was reading a story the other day, in some old book, of a moody man who was walking with a friend, and, after a long silence, suddenly cried out, as if in pain. "What ails you?" said his friend.

[13] Mary Wollstonecraft, Posthumous Works of the Author of A Vindication of the Rights of Woman (1759–1797)
  context before: This was, at first, the most bitter punishment; but sullen pride, or a kind of stupid desperation, made me, at length, almost regardless of the contempt, which had wrung from me so many solitary tears at the only moments when I was allowed to rest.
"Thus was I the mark of cruelty till my sixteenth year; and then I have only to point out a change of misery; for a period I never knew.
  PASSAGE: Allow me first to make one observation. Now I look back, I cannot help attributing the greater part of my misery, to the misfortune of having been thrown into the world without the grand support of life--a mother's affection.
  context after: I had no one to love me; or to make me respected, to enable me to acquire respect. I was an egg dropped on the sand; a pauper by nature, shunted from family to family, who belonged to nobody--and nobody cared for me.

[14] William Hazlitt, Liber Amoris, Or, The New Pygmalion (1778–1830)
  context before: The agony, the conflict of hope and fear, of adoration and jealousy is over; or it would, ere long, have ended with my life. I am no more lifted now to Heaven, and then plunged in the abyss; but I seem to have been thrown from the top of a precipice, and to lie groveling, stunned, and stupefied.
  PASSAGE: I am melancholy, lonesome, and weaker than a child. The worst is, I have no prospect of any alteration for the better: she has cut off all possibility of a reconcilement at any future period.
  context after: Were she even to return to her former pretended fondness and endearments, I could have no pleasure, no confidence in them. I can scarce make out the contradiction to myself.

[15] Abraham Lincoln, The Papers and Writings of Abraham Lincoln — Volume 6: 1862-1863 (1809–1865)
  context before: And yet it is a mistake. You are sure to be happy again.
  PASSAGE: To know this, which is certainly true, will make you some less miserable now. I have had experience enough to know what I say, and you need only to believe it to feel better at once.
  context after: The memory of your dear father, instead of an agony, will yet be a sad, sweet feeling in your heart, of a purer and holier sort than you have known before.
Please present my kind regards to your afflicted mother.

[16] Samuel Taylor Coleridge, Biographia Epistolaris, Volume 1 (1772–1834)
  context before: He is a good practical mechanic, etc., and is desirous to lay out any sum of money that is necessary. You know how long, how ardently I have wished to initiate myself in Chemical science, both for its own sake, and in no small degree likewise, my beloved friend, that I may be able to sympathize with all that you do and think.
  PASSAGE: Sympathize blindly with it all I do even "now", God knows! from the very middle of my heart's heart, but I would fain sympathize with you in the light of knowledge.
  context after: This opportunity is exceedingly precious to me, as on my own account I could not afford the least additional expense, having been already, by long and successive illnesses, thrown behindhand, so much, that for the next four or five months, I fear, let me work as hard as I can, I shall not be able to do what my heart within me "burns" to do, that is, to "concenter" my free mind to the affinities of the feelings with words and ideas under the title of "Concerning Poetry, and the nature of the Pleasures derived from it". I have faith that I do understand the subject, and I am sure that if I write what I ought to do on it, the work would supersede all the books of metaphysics, and all the books of morals too.

[17] John Adams and Abigail Adams, Familiar Letters of John Adams and His Wife Abigail Adams During the Revolution with a Memoir of Mrs. Adams (1735–1826)
  context before: My friends assure me from their observations that you must have had a good passage. God grant it, I say, but my fears and anxieties are many, very many.
  PASSAGE: I had a faith and reliance that supported me before, but now my heart so misgives me that I cannot find that confidence which I wish for.
  context after: Your letter from Cape Ann arrived and cheered my drooping spirits. Could I hear of your safe arrival, I would try to compose my agitated mind, which has horrors both day and night.

[18] John Ruskin, Hortus Inclusus Messages from the Wood to the Garden, Sent in Happy Days to the Sister Ladies of the Thwaite, Coniston (1819–1900)
  context before: Much illness and much sorrow, and then I woke up to find myself old, and as if I had lost a great part of my life. Let us hope it was not all lost.
  PASSAGE: I think you can understand me when I say that I have a great fund of love, and no one to spend it upon, because there are not any to whom I could give it fully, and I love my pets so dearly, but I dare not and cannot enjoy it fully because--they die, or get injured, and then my misery is intense.
  context after: I feel as if I could tell you much, because your sympathy is so refined and so tender and true. Cannot I be a sort of second mother to you?

[19] Lucie Duff Gordon, Letters from Egypt (1821–1869)
  context before: -
  PASSAGE: I am tolerably well, but I am growing very homesick--or rather children-sick. As the time slips on I get more and more the feeling of all I am losing of my children.
  context after: We have delicious weather here and have had all the time; there has been no cold at all this winter here.
M.

[20] Charles Dickens, The Letters of Charles Dickens. Vol. 1, 1833-1856 (1812–1870)
  context before: I was so sorry to leave you all! You can scarcely imagine what a chill and blank I felt on that Monday evening at Rockingham.
  PASSAGE: It was so sad to me, and engendered a constraint so melancholy and peculiar, that I doubt if I were ever much more out of sorts in my life.
  context after: Next morning, when it was light and sparkling out of doors, I felt more at home again. But when I came in from seeing poor dear Watson's grave, Mrs.
```

## Case 4: Sad > Lonely > Isolated

```
feeling: isolated (lonely, sad)
  what happened: I moved to a new city for university.
  because: I miss home and my family so much
  afraid it means: that I do not belong here

CANDIDATE PASSAGES
[1] Robert Browning and Elizabeth Barrett Browning, The letters of Robert Browning and Elizabeth Barrett Barrett, Vol. 1 (of 2) 1845-1846 (1812–1889)
  context before: What should make you, dearest friend, weary in your soul; or out of spirits in any way?--Do ... tell me.... I was going to write without a pause--and almost I might, perhaps, ... even as one of the two hundred of your friends, ... almost I might say out that 'Do tell me.'
  PASSAGE: Or is it (which I am inclined to think most probable) that you are tired of a same life and want change? It may happen to anyone sometimes, and is independent of your will and choice, you know--and I know, and the whole world knows: and would it not therefore be wise of you, in that case, to fold your life new again and go abroad at once?
  context after: What can make you weary in your soul, is a problem to me. You are the last from whom I should have expected such a word.

[2] Lewis Melville and Mary Wortley Montagu, Lady Mary Wortley Montague, Her Life and Letters (1689-1762) (1874–1932)
  context before: I hope it has also banished the fashion of talking all at once, which was very prevailing when I was in town, and may perhaps contribute to brotherly love and unity, which was so much declined in my memory, that it was hard to invite six people that would not, by cold looks, or piquing reflections affront one another. I suppose parties are at an end, though I fear it is the consequence of the old almanac prophecy, "Poverty brings peace"; and I fancy you really follow the French mode, and the lady keeps an assembly, that the assembly may keep the lady, and card money pay for clothes and equipage as well as cards and candles.
  PASSAGE: I find I should be as solitary in London as I am here in the country, it being impossible for me to submit to live in a drum, which I think so far from a cure of uneasiness, that it is, in my opinion, adding one more to the heap.
  context after: There are so many attached to humanity, 'tis impossible to fly from them all; but experience has confirmed to me what I always thought, that the pursuit of pleasure will be ever attended with pain, and the study of ease be most certainly accompanied with pleasures. I have had this morning as much delight in a walk in the sun as ever I felt formerly in the crowded Mall, even when I imagined I had my share of the admiration of the place, which was generally soured before I slept by the informations of my female friends, who seldom failed to tell me, it was observed, I had showed an inch above my shoe-heels, or some other criticism of equal weight, which was construed affectation, and utterly destroyed all the satisfaction my vanity had given me.

[3] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 1 (1813–1883)
  context before: I can get no real information from there. It is very long since I heard anything of you!
  PASSAGE: Alas! I am out of sorts and God-forsaken. I feel so lonely, and yet do not want to see any one. What a miserable existence!
  context after: I cannot help smiling when I read in B.'s paper the articles by R. F.'s brother-in-law; the man thinks he is going thoroughly to the bottom of the thing, because he is so moderate and cautious; he knows very little of me.

[4] Anton Chekhov, Letters to His Family and Friends (1890)
  context before: In the first place, there is cholera in Moscow and about Moscow, and it will be in our parts some day soon. In the second place, I have been appointed cholera doctor, and my section includes twenty-five villages, four factories, and one monastery.
  PASSAGE: I am organizing the building of barracks, and so on, and I feel lonely, for all the cholera business is alien to my heart, and the work, which involves continual driving about, talking, and attention to petty details, is exhausting for me.
  context after: I have no time to write. Literature has been thrown aside for a long time now, and I am poverty-stricken, as I thought it convenient for myself and my independence to refuse the remuneration received by the section doctors.

[5] George Sand and Gustave Flaubert, The George Sand-Gustave Flaubert Letters (1804–1876)
  context before: Solitude does not weigh on you? I really think that it is not absolute, and that somewhere there is a sweetheart who comes and goes, or who lives near there.
  PASSAGE: But there is something of the anchorite in your life just the same, and if envy your situation. As for me, I am too alone at Palaiseau, with a dead soul; not alone enough at Nohant, with the children whom I love too much to belong to myself,--and at Paris, one does not know what one is, one forgets oneself entirely for a thousand things which are not worth any more than oneself.
  context after: I embrace you with all my heart, dear friend; remember me to your mother, to your dear family, and write me at Nohant, that will do me good.
The cheeses?

[6] Thomas Carlyle and Ralph Waldo Emerson, The Correspondence of Thomas Carlyle and Ralph Waldo Emerson, 1834-1872, Vol. I (1795–1881)
  context before: Surely, I often say, if ever man had a finger-of-Providence shown him, thou hast it; literature will neither yield thee bread, nor a stomach to digest bread with: quit it in God's name, shouldst thou take spade and mattock instead. The truth is, I believe literature to be as good as dead and gone in all parts of Europe at this moment, and nothing but hungry Revolt and Radicalism appointed us for perhaps three generations; I do not see how a man can honestly live by writing in another dialect than that, in England at least; so that if you determine on not living dishonestly, it will behove you to look several things full in the face, and ascertain what is what with some distinctness.
  PASSAGE: I suffer also terribly from the solitary existence I have all along had; it is becoming a kind of passion with me, to feel myself among my brothers.
  context after: And then, How? Alas!

[7] Roe, Frances Marie Antoinette Mack, Army Letters from an Officer's Wife, 1871-1888 (?–1920)
  context before: Major Pierce was promoted to another regiment and we miss them very much.
FORT SHAW, MONTANA TERRITORY, July, 1882.
  PASSAGE: THE garrison seems lonesome since the two companies have been out, and I am beginning to feel that I am at home alone quite too much.
  context after: Faye was in Washington two months, and almost immediately after he got back he was ordered to command the paymaster's escort from Helena here, and now he is off again for the summer! The camp is on Birch Creek not far from the Piegan Agency.

[8] Fanny Kemble, Journal of a Residence on a Georgian Plantation: 1838-1839 (1809–1893)
  context before: Friday, March 1.--Last night after writing so much to you I felt weary, and went out into the air to refresh my spirit. The scene just beyond the house was beautiful, the moonlight slept on the broad river which here is almost the sea, and on the masses of foliage of the great southern oaks; the golden stars of German poetry shone in the purple curtains of the night, and the measured rush of the Atlantic unfurling its huge skirts upon the white sands of the beach (the sweetest and most awful lullaby in nature) resounded through the silent air.
  PASSAGE: I have not felt well, and have been much depressed for some days past. I think I should die if I had to live here.
  context after: This morning, in order not to die yet, I thought I had better take a ride, and accordingly mounted the horse which I told you was one of the equestrian alternatives offered me here; but no sooner did he feel my weight, which, after all, is mere levity and frivolity to him, than he thought proper to rebel, and find the grasshopper a burthen, and rear and otherwise demonstrate his disgust. I have not ridden for a long time now, but Montreal's opposition very presently aroused the Amazon which is both natural and acquired in me, and I made him comprehend that, though I object to slaves, I expect obedient servants; which views of mine being imparted by a due administration of both spur and whip, attended with a judicious combination of coaxing pats on his great crested neck, and endearing commendations of his beauty, produced the desired effect.

[9] Walter Scott, The Journal of Sir Walter Scott From the Original Manuscript at Abbotsford (1771–1832)
  context before: February 12.--Having ended the second volume of Woodstock last night, I have to begin the third this morning. Now I have not the slightest idea how the story is to be wound up to a catastrophe.
  PASSAGE: I am just in the same case as I used to be when I lost myself in former days in some country to which I was a stranger.
  context after: I always pushed for the pleasantest road, and either found or made it the nearest. It is the same in writing, I never could lay down a plan--or, having laid it down, I never could adhere to it; the action of composition always diluted some passages, and abridged or omitted others; and personages were rendered important or insignificant, not according to their agency in the original conception of the plan, but according to the success, or otherwise, with which I was able to bring them out.

[10] Charles Lever, Charles Lever, His Life in His Letters, Vol. II (1806–1872)
  context before: “Croce di Malta, Spezzia, Dec. 30, 1866.
“Your last pleasant note and its ‘stuffing’ has just reached me here, where I am consularising, bullying Custom-house folk, and playing the devil with all the authorities to show my activity in the public service.
  PASSAGE: I can’t endure being away from home and my old routine life; but there was no help for it, and I am here now for another week to come.
  context after: “The name I want for the author of Tony is ‘Arthur Helsham,’ the name of my mother’s family; and the last man who bore the aforesaid was the stupidest blockhead of the house, and the luckiest too. Faustum sit augurium.

[11] Elizabeth Barrett Browning, The Letters of Elizabeth Barrett Browning (Volume 2 of 2) (1806–1861)
  context before: We have done duty to the north too lately. Now it seems to me we have the right (of virtue, in spite of what I said on another page, or rather, because I said it in good human inconsistency), the right to have and hold our Italy in undisturbed possession.
  PASSAGE: I never feel at home anywhere else, or to live rightly anywhere else at all. It's a horrible want of patriotism, of course, only, if I were upon trial, I might say in a low voice a few things to soften the judgment against me on account of that sin.
  context after: Ah! we missed you at Havre! If you had come it would have been something pleasant to remember that detestable place by, besides the salt-water which profited one's health a little.

[12] Charles Lamb and Mary Lamb, The Works of Charles and Mary Lamb — Volume 6 Letters 1821-1842 (1775–1834)
  context before: -
  PASSAGE: We are in the House, that is all. I hope one day we shall both enjoy it, and see our friends again. But till then I must be a solitary nurse.
  context after: I am trying Becky's sister to be with her, so don't say anything to Miss James.

[13] Sarah Morgan Dawson, A Confederate Girl's Diary (1842–1909)
  context before: Nolan's plantation, with Baton Rouge lying just seven miles from us to the east. We can surely hear the cannon from here.
  PASSAGE: They are all so kind to us that I ought to be contented; but still I wish I was once more at home. I suppose it is very unreasonable in me, but I cannot help it.
  context after: I miss my old desk very much; it is so awkward to write on my knee that I cannot get used to it. Mine is a nice little room upstairs, detached from all the rest, for it is formed by a large dormer window looking to the north, from which I have seen a large number of guerrillas passing and repassing in their rough costumes, constantly.

[14] Ambrose Bierce, The Letters of Ambrose Bierce, With a Memoir by George Sterling (1842–1914)
  context before: What do I think of Edith Wharton? Just what Pollard thought--see Their Day in Court, which I think you have.
  PASSAGE: I fear you have the wanderlust incurably. I never had it bad, and have less of it now than ever before. I shall not see California again.
  context after: My love to all your family goes with this, and to you all that you will have.

[15] John Adams and Abigail Adams, Familiar Letters of John Adams and His Wife Abigail Adams During the Revolution with a Memoir of Mrs. Adams (1735–1826)
  context before: We have had four of the coldest days I ever knew, and they were followed by the severest snow-storm I ever remember. The wind, blowing like a hurricane for fifteen or twenty hours, rendered it impossible for man or beast to live abroad, and has blocked up the roads so that they are impassable.
  PASSAGE: A week ago I parted with my daughter, at the request of our Plymouth friends, to spend a month with them; so that I am solitary indeed.
  context after: Can the best of friends recollect that for fourteen years past I have not spent a whole winter alone? Some part of the dismal season has heretofore been mitigated and softened by the social converse and participation of the friend of my youth.

[16] Arthur Christopher Benson, The Upton Letters (1862–1925)
  context before: As a counterpoise to this I like to think of all the happiness flowing into hundreds of homes; the father and mother waiting for the sound of the wheels that bring the boy back; the children who have gone down to the lodge to welcome the big brothers with shouts and kisses; and the boy himself, with all the dear familiar scene and home faces opening out before him. We ought not to grudge the loneliness here before the thought of all those old and blessed joys of life that are being renewed elsewhere.
  PASSAGE: But I am here, a lonely man, wondering and doubting and desiring I hardly know what. Some nearness of life, some children of my own.
  context after: You are apt to think of yourself as shelved and isolated; yet, after all, you have the real thing--wife, children, and home. But, in my case, these boys who are dear to me have forgotten me already.

[17] John Keats, Letters to His Family and Friends (1819)
  context before: I wish I had money enough to do nothing but travel about for years. Were you now in England I dare say you would be able (setting aside the pleasure you would have in seeing your mother) to suck out more amusement for society than I am able to do.
  PASSAGE: To me it is all as dull here as Louisville could be. I am tired of the theatres. Almost all the parties I may chance to fall into I know by heart.
  context after: I know the different styles of talk in different places,--what subjects will be started, how it will proceed like an acted play, from the first to the last act. If I go to Hunt's I run my head into many tunes heard before, old puns, and old music; to Haydon's worn-out discourses of poetry and painting.

[18] William Hazlitt, Liber Amoris, Or, The New Pygmalion (1778–1830)
  context before: I wept myself almost blind, and I gazed at the broad golden sunset through my tears that fell in showers. As I trod the green mountain turf, oh! how I wished to be laid beneath it—in one grave with her—that I might sleep with her in that cold bed, my hand in hers, and my heart for ever still—while worms should taste her sweet body, that I had never tasted!
  PASSAGE: There was a time when I could bear solitude; but it is too much for me at present. Now I am no sooner left to myself than I am lost in infinite space, and look round me in vain for suppose or comfort.
  context after: She was my stay, my hope: without her hand to cling to, I stagger like an infant on the edge of a precipice. The universe without her is one wide, hollow abyss, in which my harassed thoughts can find no resting-place.

[19] Alfred Russel Wallace and James Marchant, Alfred Russel Wallace: Letters and Reminiscences, Vol. 1 (1823–1913)
  context before: In the country between Ega and Peru there is work for fifty collectors for fifty years. There are hundreds and thousands of Andean valleys every one of which would bear exploring.
  PASSAGE: Here it is the same with islands. I could spend twenty years here were life long enough, but feel I cannot stand it, away from home and books and collections and comforts, more than four or five, and then I shall have work to do for the rest of my life.
  context after: What would be the use of accumulating materials which one could not have time to work up? I trust your brother may give us a grand and complete work on the Coleoptera of the Amazon Valley, if not of all South America....--Yours faithfully,

[20] Nathaniel Hawthorne, Passages from the American Notebooks, Volume 2. (1804–1864)
  context before: If we were to travel a thousand miles, we could not escape the world more completely than we can here.
* * * * * *
  PASSAGE: I read no newspapers, and hardly remember who is President, and feel as if I had no more concern with what other people trouble themselves about than if I dwelt in another planet.
  context after: May 1st.--. . . . Every day of my life makes me feel more and more how seldom a fact is accurately stated; how, almost invariably, when a story has passed through the mind of a third person, it becomes, so far as regards the impression that it makes in further repetitions, little better than a falsehood, and this, too, though the narrator be the most truth-seeking person in existence.
```

## Case 5: Sad > Bored > Apathetic

```
feeling: apathetic (bored, sad)
  what happened: I am doing everything I am supposed to do.
  because: none of it feels like it matters
  afraid it means: that my life has no point

CANDIDATE PASSAGES
[1] Mark Twain, Mark Twain's Letters — Volume 2 (1867-1875) (1835–1910)
  context before: I wish I had gone to Washington in the winter instead of going West. I could have gouged an office out of Bill Stewart for him, and that would atone for the loss of my home visit.
  PASSAGE: But I am so worthless that it seems to me I never do anything or accomplish anything that lingers in my mind as a pleasant memory.
  context after: My mind is stored full of unworthy conduct toward Orion and towards you all, and an accusing conscience gives me peace only in excitement and restless moving from place to place. If I could say I had done one thing for any of you that entitled me to your good opinion, (I say nothing of your love, for I am sure of that, no matter how unworthy of it I may make myself, from Orion down you have always given me that, all the days of my life, when God Almighty knows I seldom deserve it,) I believe I could go home and stay there and I know I would care little for the world's praise or blame.

[2] Henri Frédéric Amiel, Amiel's Journal: The Journal Intime of Henri-Frédéric Amiel (1821–1881)
  context before: -
  PASSAGE: Do I feel any relief, any joy, pride, hope? Hardly. It seems to me that I feel nothing at all, or at least my feeling is so vague and doubtful that I cannot analyze it.
  context after: On the whole, I am rather tempted to say to myself, how much labor for how small a result--Much ado about nothing! And yet the work in itself is good, is successful.

[3] Anton Chekhov, Letters to His Family and Friends (1890)
  context before: I am afraid that in this respect I resemble Gontcharov, whom I don’t like, who is ten heads taller than I am in talent. I have not enough passion; add to that this sort of lunacy: for the last two years I have for no reason at all ceased to care about seeing my work in print, have become indifferent to reviews, to literary conversations, to gossip, to success and failure, to good pay--in short, I have gone downright silly.
  PASSAGE: There is a sort of stagnation in my soul. I explain it by the stagnation in my personal life. I am not disappointed, I am not tired, I am not depressed, but simply everything has suddenly become less interesting.
  context after: I must do something to rouse myself.

[4] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 1 (1813–1883)
  context before: Or shall I look on indifferently, amuse myself when I can make a hundred thalers, buy champagne, and turn my back upon the world? It is a misery.
  PASSAGE: I am going from bad to worse every day, and lead an indescribably worthless life. Of real enjoyment of life I know nothing; to me "enjoyment of life, of love," is a matter of imagination, not of experience.
  context after: In this manner my heart has to go to my brain, and my life becomes an artificial one; only as an "artist" I can live; in the artist my whole "man" has been sunk.
If I could visit you in Weimar and see a performance of my operas now and then, I might perhaps still hope to recover.

[5] John Keats, Letters to His Family and Friends (1819)
  context before: The reason of my delaying is oftentimes from this feeling,--I wait for a proper temper. Now you ask for an immediate answer, I do not like to wait even till to-morrow.
  PASSAGE: However, I am now so depressed that I have not an idea to put to paper--my hand feels like lead--and yet it is an unpleasant numbness; it does not take away the pain of Existence.
  context after: I don't know what to write.

[6] Alexander Whyte, Samuel Rutherford and Some of His Correspondents (1836–1921)
  context before: We used to talk in dear old John Meine's back-shop on week-nights and upstairs on Sabbath nights about these things. And long as it is since we saw much of one another, I feel that you know me out and in, and through and through, as no one else knows me.
  PASSAGE: Tell me, then, what I am to do with myself. I will try to do what you tell me, for I am wearied and worn out with my stagnant and miserable life.
  context after: Pity me, Mr. Samuel, my honoured and dear friend, for my pirn is almost run out, and I am not near saved.'

[7] Charles Darwin, More Letters of Charles Darwin — Volume 2 A Record of His Work in a Series of Hitherto Unpublished Letters (1809–1882)
  context before: Even their size must be very inconvenient. You and Bentham must hate the monocotyledons, for what work the Orchideae must have been, and Gramineae and Cyperaceae will be.
  PASSAGE: I am rather despondent about myself, and my troubles are of an exactly opposite nature to yours, for idleness is downright misery to me, as I find here, as I cannot forget my discomfort for an hour.
  context after: I have not the heart or strength at my age to begin any investigation lasting years, which is the only thing which I enjoy; and I have no little jobs which I can do. So I must look forward to Down graveyard as the sweetest place on earth.

[8] Louis Agassiz, Louis Agassiz: His Life and Correspondence (1807–1873)
  context before: It is a great pleasure to have at least a part of our Swiss mountains always in sight. To enjoy it the more, I have placed my table opposite the window, so that every time I lift my head my eyes rest on our dear country.
  PASSAGE: This does not prevent me from feeling dull sometimes, especially when I am alone, but I hope this will pass off when my occupations become more regular. . .
  context after: A far more stimulating intellectual life than that of Heidelberg awaited our students at Munich. Among their professors were some of the most original men of the day,--men whose influence was felt all over Europe.

[9] Raden Adjeng Kartini, Letters of a Javanese Princess (1879–1904)
  context before: I deserve a fine scolding for my long delay in writing; in large measure, it was due to indolence. I am not satisfied with myself!
  PASSAGE: What makes me so lazy and restless? I do not understand it. I am not definitely sick, but at the same time I am far from well.
  context after: I am dull, weary and uneasy; nonsense--hypochondria--there! I must seize hold of myself; it is work that I need--work that my heart is in.

[10] Walter Scott, The Journal of Sir Walter Scott From the Original Manuscript at Abbotsford (1771–1832)
  context before: At returning settled with Chief-Commissioner that I should receive him on 26th December at Abbotsford.
After all, may there not be, in this failure to please, some reliques of the very unfavourable matters in which I have been engaged of late,--the threat of imprisonment, the resolution to become insolvent?
  PASSAGE: I cannot feel that there is. What I suffer by is the difficulty of not setting my foot upon such ground as I have trod before, and thus instead of attaining novelty I lose spirit and nature.
  context after: On the other hand, who would 'thank me for "repented sheets"? Here is a good joke enough, lost to all who have not known the Clerk's table before the Jurisdiction Act.

[11] George Sand and Gustave Flaubert, The George Sand-Gustave Flaubert Letters (1804–1876)
  context before: Perhaps those which I like are the worst. But I have stopped worrying about myself, so far as I have ever done so.
  PASSAGE: Life has always taken me out of myself, and so it will to the end. My heart is always affected to the detriment of my head.
  context after: At present it is my little children who devour all my intellect; Aurore is a jewel, a nature before which I bow in admiration; will it last like that?
You are going to spend the winter in Paris, and I, I don't know when I shall go.

[12] Fanny Kemble, Records of Later Life (1809–1893)
  context before: I have had a letter from the Leamington manager, desiring me to act there, which I will do, some time or other.
I have a riding-habit of my own, and need not hire one at Hastings; but I shall be glad to hire a horse while I am with you, as, you know, I do not mind riding alone....
  PASSAGE: I feel intensely stupid, which makes me think I must be ill (admire, I beg, the conceit of that inference), as I have no other symptoms of indisposition.
  context after: Farewell. Give my love to Dorothy.

[13] Arthur Christopher Benson, The Upton Letters (1862–1925)
  context before: Well, then, a few days ago I woke early, after troubled dreams, and knew that the old enemy had clutched me. I lay in a strange agony of mind, my heart beating thick, and with an insupportable weight on my heart.
  PASSAGE: It always takes the same form with me--an overwhelming sense of failure in all that I attempt, a dreary consciousness of absolute futility, coupled with the sense of the brevity and misery of human life generally.
  context after: I ask myself what is the use of anything? What is an almost demoniacal feature of the mood is that it lays a spell of utter dreariness upon all pleasures as well as duties.

[14] Charles Lever, Charles Lever, His Life in His Letters, Vol. II (1806–1872)
  context before: “A Mr Crane, West George Street, Glasgow, writes me a very courteous note, and says, ‘I do thank the Editor of “Blackwood” for publishing what you say of Scott,’ and goes on to express his hearty concurrence with it all, and he regrets that it had not been spoken instead of written, &c, &c.
“I do not feel as if I was to get better this time; but I have called wolf so often I shall scream no more.
  PASSAGE: What I feel most, and struggle against most in vain, is depression. I have got to believe not only that my brains are leaving me, but that my friends are tired of me.
  context after: Of course, I couple the two disasters together, and long to be beyond the reach of remembering either one or the other.
“You read my MS. so easily that if you do not like the O’D. don’t print it--it saves me a disappointment at least; and above all, do not mind any chance irritability I display in writing, for a cry escapes me in my pain, and I often do not hear it myself.

[15] Forbes Robinson, Letters to His Friends (1867–1904)
  context before: -
  PASSAGE: . . . I do feel for you, and could do a great deal to help you. I can only tell you what I have felt to be the only thing which makes life endurable at a time of real sorrow--God Himself.
  context after: He comes unutterably near in trouble. In fact, one scarcely knows He exists until one loves or sorrows.

[16] Charles Lamb and Mary Lamb, The Works of Charles and Mary Lamb — Volume 5 The Letters of Charles and Mary Lamb, 1796-1820 (1775–1834)
  context before: Your kind heart will, I know, even if you have been a little displeased, forgive me, when I assure you my spirits have been so much hurt by my last illness, that at times I hardly know what I do. I do not mean to alarm you about myself, or to plead an excuse; but I am very much otherwise than you have always known me.
  PASSAGE: I do not think any one perceives me altered, but I have lost all self-confidence in my own actions, and one cause of my low spirits is, that I never feel satisfied with any thing I do--a perception of not being in a sane state perpetually haunts me.
  context after: I am ashamed to confess this weakness to you; which, as I am so sensible of, I ought to strive to conquer. But I tell you, that you may excuse any part of my letter that has given offence: for your not answering it, when you are such a punctual correspondent, has made me very uneasy.

[17] Ulysses S. Grant, Letters of Ulysses S. Grant to his father and his youngest sister, 1857-78 (1822–1885)
  context before: I have now been home nearly a week, but return to Springfield to-day. I have tendered my services to the Government and go to-day to make myself useful, if possible, from this until all our National difficulties are ended.
  PASSAGE: During the six days I have been at home I have felt all the time as if a duty were being neglected that was paramount to any other duty I ever owed.
  context after: I have every reason to be well satisfied with myself for the services already rendered, but to stop now would not do.
All here are well.

[18] William Hazlitt, Liber Amoris, Or, The New Pygmalion (1778–1830)
  context before: Am I not hated, repulsed, derided by her whom alone I love or ever did love? I cannot stay in any place, and seek in vain for relief from the sense of her contempt and her ingratitude.
  PASSAGE: I can settle to nothing: what is the use of all I have done? Is it not that very circumstance (my thinking beyond my strength, my feeling more than I need about so many things) that has withered me up, and made me a thing for Love to shrink from and wonder at?
  context after: Who could ever feel that peace from the touch of her dear hand that I have done; and is it not torn from me for ever? My state is this, that I shall never lie down again at night nor rise up in the morning in peace, nor ever behold my little boy’s face with pleasure while I live—unless I am restored to her favour.

[19] Robert Browning and Elizabeth Barrett Browning, The letters of Robert Browning and Elizabeth Barrett Barrett, Vol. 1 (of 2) 1845-1846 (1812–1889)
  context before: I would rather write than not--I! But to be written to is the chief gladness of course; and with all you say of liking to have my letters (which I like to hear quite enough indeed) you cannot pretend to think that yours are not more to me, most to me!
  PASSAGE: Ask my guardian-angel and hear what he says! Yours will look another way for shame of measuring joys with him! Because as I have said before, and as he says now, you are all to me, all the light, all the life; I am living for you now.
  context after: And before I knew you, what was I and where? What was the world to me, do you think? and the meaning of life?

[20] Mary Wollstonecraft, Posthumous Works of the Author of A Vindication of the Rights of Woman (1759–1797)
  context before: I am really unable to bear the continual inquietude which your and ------'s never-ending plans produce. This you may term want of firmness--but you are mistaken--I have still sufficient firmness to pursue my principle of action.
  PASSAGE: The present misery, I cannot find a softer word to do justice to my feelings, appears to me unnecessary--and therefore I have not firmness to support it as you may think I ought.
  context after: I should have been content, and still wish, to retire with you to a farm--My God! any thing, but these continual anxieties--any thing but commerce, which debases the mind, and roots out affection from the heart.
I do not mean to complain of subordinate inconveniences----yet I will simply observe, that, led to expect you every week, I did not make the arrangements required by the present circumstances, to procure the necessaries of life.
```

## Case 6: Mad > Hurt > Distant

```
feeling: distant (hurt, mad)
  what happened: I said something cruel to my brother and now he won't speak to me.
  because: I lost my temper
  afraid it means: that I have ruined the relationship for good

CANDIDATE PASSAGES
[1] Samuel Pepys, Diary of Samuel Pepys — Volume 26: January/February 1663-64 (1633–1703)
  context before: Creed most excellently writ, both showing his stoutness and yet willingness to peace, reproaching me yet flattering me again, and in a word in as good a manner as I think the world could have wrote, and indeed put me to a greater stand than ever I thought I could have been in this matter. All the morning thinking how to behave myself in the business, and at noon to the Coffee-house; thence by his appointment met him upon the 'Change, and with him back to the Coffee-house, where with great seriousness and strangeness on both sides he said his part and I mine, he sometimes owning my favour and assistance, yet endeavouring to lessen it, as that the success of his business was not wholly or very much to be imputed to that assistance: I to alledge the contrary, and plainly to tell him that from the beginning I never had it in my mind to do him all that kindnesse for nothing, but he gaining 5 or L600, I did expect a share of it, at least a real and not a complimentary acknowledgment of it.
  PASSAGE: In fine I said nothing all the while that I need fear he can do me more hurt with them than before I spoke them.
  context after: The most I told him was after we were come to a peace, which he asked me whether he should answer the Board's letter or no. I told him he might forbear it a while and no more.

[2] Elizabeth Barrett Browning, The Letters of Elizabeth Barrett Browning (Volume 2 of 2) (1806–1861)
  context before: It is one of the beatitudes of art, and attainable without putting off the flesh.
To be plain, and not mystical, it is obvious that if I had expected compliments and caresses from the English press to my 'Poems before Congress,' the said poems would have been little deserved in England, and a greater mistake on my part than any committed by the 'Athenæum,' which is saying much.
  PASSAGE: There! I have done. The spark is under my shoe. If in 'losing my temper' I have 'lost my music,' don't let it be said that I have lost my friend by my own fault and choice also.
  context after: For I would not willingly lose him, though he should be unjust to me thrice, instead of this once throughout our intercourse. Affectionately yours, dear Mr.

[3] Richard Harding Davis, Adventures and Letters of Richard Harding Davis (1864–1916)
  context before: I got your letters late last night and they made me pretty solemn. It is an awfully solemn thing to have people care for you like that and to care for them as I do.
  PASSAGE: I can't tell you how much I love you. You don't know how much the pain of worrying you for a month has meant to me, but I have talked it all out with myself, and left it to God and I am sure I am doing right.
  context after: As Mrs. Crown said, "There's a whole churchful up here praying for you," and I guess that will pull me through.

[4] Jonathan Swift, The Journal to Stella (1667–1745)
  context before: Upon my advice they both came to Ireland, and have been ever since my constant companions; and the remainder of my life will be a very melancholy scene, when one of them is gone, whom I most esteemed, upon the score of every good quality that can possibly recommend a human creature.” He would not for the world be present at her death: “I should be a trouble to her, and a torment to myself.” If Stella came to Dublin, he begged that she might be lodged in some airy, healthy part, and not in the Deanery, where too it would be improper for her to die. “There is not a greater folly,” he thinks, “than to contract too great and intimate a friendship, which must always leave the survivor miserable.” To Dr. Stopford he wrote in similar terms of the “younger of the two” “oldest and dearest friends I have in the world.” “This was a person of my own rearing and instructing from childhood, who excelled in every good quality that can possibly accomplish a human creature. . . .
  PASSAGE: I know not what I am saying; but believe me that violent friendship is much more lasting and as much engaging as violent love.” To Dr.
  context after: Sheridan he said, “I look upon this to be the greatest event that can ever happen to me; but all my preparation will not suffice to make me bear it like a philosopher nor altogether like a Christian. There hath been the most intimate friendship between us from our childhood, and the greatest merit on her side that ever was in one human creature towards another.” {0j} Pope alludes in a letter to Sheridan to the illness of Swift’s “particular friend,” but with the exception of another reference by Pope, and of a curiously flippant remark by Bolingbroke, the subject is nowhere mentioned in Swift’s correspondence with his literary and fashionable friends in London.

[5] Walter Scott, The Journal of Sir Walter Scott From the Original Manuscript at Abbotsford (1771–1832)
  context before: But nature has given me a kind of buoyancy, I know not what to call it, that mingles even with my deepest afflictions and most gloomy hours. I have a secret pride--I fancy it will be so most truly termed--which impels me to mix with my distresses strange snatches of mirth "which have no mirth in them."
  PASSAGE: In fact, the journey hither, the absence of the affectionate friend that used to be my companion on the journey, and many mingled thoughts of bitterness, have given me a fit of the bile.
  context after: -

[6] H. M. Tomlinson, The Sea and the Jungle (1873–1958)
  context before: I know her. She is not exactly all she should be, but I apprehend exactly what she is.
  PASSAGE: If I hurt myself against her it is my own fault. She is as familiar to me as home now. I should resent any alteration.
  context after: Having learned to know her faults I like her as she is; the trestle bridge with its sagging hand-ropes and wobbling stanchions (look out, you, when she rolls) which crosses the main deck aft on the port side from the amidships section, where I live, to the poop, where the Doctor lives. The two little streets of three doors each, to port and starboard of her amidships, the doors that open out under the shade of the boat deck to sea.

[7] Sarah Morgan Dawson, A Confederate Girl's Diary (1842–1909)
  context before: "And our entire conversation was about you," she said, as though to flatter my vanity immensely. He told her then that he had written repeatedly to me, without receiving an answer, and at last had written again, in which he had used some expressions which he feared had offended my reserved disposition.
  PASSAGE: Something had made me angry, for without returning letter or message to say I was not displeased, I had maintained a resolute silence, which had given him more pain and uneasiness than he could say.
  context after: That during all this time he had had no opportunity of explaining it to me, and that now he begged her to tell me that he would not offend me for worlds--that he admired me more than any one he had ever met, that he could not help saying what he did, but was distressed at offending me, etc. The longest explanation!

[8] John Adams and Abigail Adams, Familiar Letters of John Adams and His Wife Abigail Adams During the Revolution with a Memoir of Mrs. Adams (1735–1826)
  context before: My friends assure me from their observations that you must have had a good passage. God grant it, I say, but my fears and anxieties are many, very many.
  PASSAGE: I had a faith and reliance that supported me before, but now my heart so misgives me that I cannot find that confidence which I wish for.
  context after: Your letter from Cape Ann arrived and cheered my drooping spirits. Could I hear of your safe arrival, I would try to compose my agitated mind, which has horrors both day and night.

[9] Alexis de Tocqueville and Nassau William Senior, Correspondence & Conversations of Alexis de Tocqueville with Nassau William Senior from 1834 to 1859, Volume 2 (1805–1859)
  context before: I have not either much to boast of on the score of health since we parted. The illness which I had in Paris became still worse, and when I got a little better in that way I had a violent bronchial attack.
  PASSAGE: I even began to spit blood, which had not happened to me for many years, and I am still almost reduced to silence. Still I am beginning to mend, and I hope, please God, to be able to speak to my friends when they visit me.
  context after: You are aware that I wished to induce my wife to accompany me to the South; but the length of the journey, the difficulties of transport, the heat, and indeed the state of my health, were reasons which she brought forward with so much force that we have remained here, and shall not leave till the end of September. We still hope that you and Miss Senior will join us the first week in that month.

[10] Ambrose Bierce, The Letters of Ambrose Bierce, With a Memoir by George Sterling (1842–1914)
  context before: Thank you so much for the books and the inscription--which (as do all other words of praise) affects me with a sad sense of my shortcomings as writer and man. Things of that kind from too partial friends point out to me with a disquieting significance what I ought to be; and the contrast with what I am hurts.
  PASSAGE: Maybe you feel enough that way sometimes to understand. You are still young enough to profit by the pain; my character is made--my opportunities are gone.
  context after: But it does not greatly matter--nothing does. I have some little testimony from you and Scheff and others that I have not lived altogether in vain, and I know that I have greater satisfaction in my slight connection with your and their work than in my own.

[11] Robert Louis Stevenson, The Works of Robert Louis Stevenson - Swanston Edition, Vol. 23 (1850–1894)
  context before: But thanks to George Sand and the sunshine, I am very jolly.
That last word was so much out of key that I could sit no longer, and went away to seek out my clergyman and apologise to him.
  PASSAGE: He was gone to bed. I don't know what makes me take this so much to heart. I suppose it's nerves or pride or something; but I am unhappy about it.
  context after: I am going to drown my sorrows in Consuelo and burn some incense in my pipe to the god of Contentment and Forgetfulness.
I do not know, but I hope, if I can only get better, I shall be a help to you soon in every way and no more a trouble and burthen.

[12] Ludwig van Beethoven, Beethoven's Letters 1790-1826, Volume 1 (1770–1827)
  context before: I send you "Kennst Du das Land," written with my own hand, as a remembrance of the hour when I first knew you; I send you also another that I composed since I bade you farewell, my dearest, fairest sweetheart!
Herz, mein Herz, was soll das geben, Was bedränget dich so sehr; Welch ein neues fremdes Leben, Ich erkenne dich nicht mehr.
  PASSAGE: Now answer me, my dearest friend, and say what is to become of me since my heart has turned such a rebel. Write to your most faithful friend,
  context after: -

[13] Raden Adjeng Kartini, Letters of a Javanese Princess (1879–1904)
  context before: Day and night I wonder by what means our ancient traditions could be overcome. For myself, I could find a way to shake them off, to break them, were it not that another bond, stronger than any age-old tradition could ever be, binds me to my world; and that is the love which I bear for those to whom I owe my life, and whom I must thank for everything.
  PASSAGE: Have I the right to break the hearts of those who have given me nothing but love and kindness my whole life long, and who have surrounded me with the tenderest care?
  context after: But it was not the voices alone which reached me from that distant, that bright, that new-born Europe, which made me long for a change in existing conditions. Even in my childhood, the word "emancipation" enchanted my ears; it had a significance that nothing else had, a meaning that was far beyond my comprehension, and awakened in me an evergrowing longing for freedom and independence--a longing to stand alone.

[14] Fanny Burney, The Diary and Letters of Madame D'Arblay — Volume 1 (1752–1840)
  context before: Wellbeck-st., NO, 33, Cavendish-sq.,
Friday, Aug. 13, 1784.
  PASSAGE: Give yourself no serious concern, sweetest Burney. All is well, and I am too happy myself to make a friend otherwise; quiet your kind heart immediately, and love my husband if you love his and your H.
  context after: L. Piozzi.

[15] William Hazlitt, Liber Amoris, Or, The New Pygmalion (1778–1830)
  context before: The agony, the conflict of hope and fear, of adoration and jealousy is over; or it would, ere long, have ended with my life. I am no more lifted now to Heaven, and then plunged in the abyss; but I seem to have been thrown from the top of a precipice, and to lie groveling, stunned, and stupefied.
  PASSAGE: I am melancholy, lonesome, and weaker than a child. The worst is, I have no prospect of any alteration for the better: she has cut off all possibility of a reconcilement at any future period.
  context after: Were she even to return to her former pretended fondness and endearments, I could have no pleasure, no confidence in them. I can scarce make out the contradiction to myself.

[16] Napoleon I, Emperor of the French, Napoleon's Letters to Josephine, 1796-1812 For the First Time Collected and Translated, with Notes Social, Historical, and Chronological, from Contemporary Sources (1769–1821)
  context before: You have shown courage; it is necessary that you should maintain it and not give way to a doleful melancholy. You must be contented and take special care of your health, which is so precious to me.
  PASSAGE: If you are attached to me and if you love me, you should show strength of mind and force yourself to be happy. You cannot question my constant and tender friendship, and you would know very imperfectly all the affection I have for you if you imagined that I can be happy if you are unhappy, and contented if you are ill at ease.
  context after: Adieu, dear. Sleep well; dream that I wish it.

[17] Forbes Robinson, Letters to His Friends (1867–1904)
  context before: I tell you what has been the greatest possible strength to me of late. God is not merely a Person, He is Three Persons in One.
  PASSAGE: I am always trying to get closer to those whom I love best, to know them more, to serve them better. Yet something is ever keeping us apart.
  context after: I said 'something,' I mean 'some one,' for only a person can keep a person from another--only a malicious, a devilish person--yet I feel that some day I shall be able to love, and know them better. Then I look out on life and I see how again and again death, and some one worse than death, is separating us, misinterpreting motives, keeping men apart; men are struggling to be one, and cannot be; on earth persons long to be one, persons who love feel they ought to be, they must be one.

[18] Marcus Tullius Cicero, The Letters of Cicero, Volume 1 The Whole Extant Correspodence in Chronological Order (107 BC–44 BC)
  context before: I was doing so before spontaneously, and have been since greatly stirred by your two letters, with their earnest expressions to the same effect. Besides, Sallustius has been always at my side to prompt me to spare no pains to induce Lucceius to be reconciled to you.
  PASSAGE: But after doing everything that could be done, not only did I fail to renew his old feelings towards you, but I could not even succeed in eliciting the reason of his alienation.
  context after: On his part, however, he keeps harping on that arbitration case of his, and the other matters which I knew very well before you left Rome were causing him offence. Still, he has certainly got something else fixed deeper in his mind; and this no letters from you, and no commissioning of me will obliterate as easily as you will do in a personal interview, I don't mean merely by your words, but by the old familiar expression of your face--if only you think it worth while, as you will if you will listen to me, and be willing to act with your habitual kindness.

[19] Henri Frédéric Amiel, Amiel's Journal: The Journal Intime of Henri-Frédéric Amiel (1821–1881)
  context before: Pain seems to me a punishment and not a mercy: this is why I have a secret horror of it. And as I feel myself vulnerable at all points, and everywhere accessible to pain, I prefer to remain motionless, like a timid child, who, left alone in his father’s laboratory, dares not touch anything for fear of springs; explosions, and catastrophes, which may burst from every corner at the least movement of his inexperienced hands.
  PASSAGE: I have trust in God directly and as revealed in nature, but I have a deep distrust of all free and evil agents. I feel or foresee evil, moral and physical, as the consequence of every error, fault, or sin, and I am ashamed of pain.
  context after: At bottom, is it not a mere boundless self-love, the purism of perfection, an incapacity to accept our human condition, a tacit protest against the order of the world, which lies at the root of my inertia? It means all or nothing, a vast ambition made inactive by disgust, a yearning that cannot be uttered for the ideal, joined with an offended dignity and a wounded pride which will have nothing to say to what they consider beneath them.

[20] Robert Browning and Elizabeth Barrett Browning, The letters of Robert Browning and Elizabeth Barrett Barrett, Vol. 1 (of 2) 1845-1846 (1812–1889)
  context before: No, you did not. Yet I am ready to repeat of myself as of others, that if I ceased to love you, I certainly would act out the whole consequence--but that is an impossible 'if' to my nature, supposing the conditions of it otherwise to be probable.
  PASSAGE: I never loved anyone much and ceased to love that person. Ask every friend of mine, if I am given to change even in friendship!
  context after: And to you...! Ah, but you never think of such a thing seriously--and you are conscious that you did not say it very sagely.
```

## Case 7: Scared > Anxious > Overwhelmed

```
feeling: overwhelmed (anxious, scared)
  what happened: My rent has gone up again and I am already in my overdraft.
  because: I cannot see how I will pay
  afraid it means: that I will lose my home

CANDIDATE PASSAGES
[1] Charles Dickens, The Letters of Charles Dickens. Vol. 2, 1857-1870 (1812–1870)
  context before: You know that you are one of many heavy charges on me, and that I trust to your so exercising your abilities and improving the advantages of your past expensive education, as soon to diminish this charge. I say no more on that head.
  PASSAGE: Whatever you do, above all other things keep out of debt and confide in me. If you ever find yourself on the verge of any perplexity or difficulty, come to me.
  context after: You will never find me hard with you while you are manly and truthful.
As your brothers have gone away one by one, I have written to each of them what I am now going to write to you.

[2] Robert Louis Stevenson, The Works of Robert Louis Stevenson - Swanston Edition, Vol. 24 (1850–1894)
  context before: -
  PASSAGE: A word in your ear: I don't like trying to support myself. I hate the strain and the anxiety; and when unexpected expenses are foisted on me, I feel the world is playing with false dice.--Now I must Tush, adieu.
  context after: -

[3] Fanny Kemble, Journal of a Residence on a Georgian Plantation: 1838-1839 (1809–1893)
  context before: Friday, March 1.--Last night after writing so much to you I felt weary, and went out into the air to refresh my spirit. The scene just beyond the house was beautiful, the moonlight slept on the broad river which here is almost the sea, and on the masses of foliage of the great southern oaks; the golden stars of German poetry shone in the purple curtains of the night, and the measured rush of the Atlantic unfurling its huge skirts upon the white sands of the beach (the sweetest and most awful lullaby in nature) resounded through the silent air.
  PASSAGE: I have not felt well, and have been much depressed for some days past. I think I should die if I had to live here.
  context after: This morning, in order not to die yet, I thought I had better take a ride, and accordingly mounted the horse which I told you was one of the equestrian alternatives offered me here; but no sooner did he feel my weight, which, after all, is mere levity and frivolity to him, than he thought proper to rebel, and find the grasshopper a burthen, and rear and otherwise demonstrate his disgust. I have not ridden for a long time now, but Montreal's opposition very presently aroused the Amazon which is both natural and acquired in me, and I made him comprehend that, though I object to slaves, I expect obedient servants; which views of mine being imparted by a due administration of both spur and whip, attended with a judicious combination of coaxing pats on his great crested neck, and endearing commendations of his beauty, produced the desired effect.

[4] Elizabeth Barrett Browning, The Letters of Elizabeth Barrett Browning (Volume 1 of 2) (1806–1861)
  context before: That song would be eminently sweet for a common writer, but Tennyson has done better, surely; his eminences are to be seen above. As for the laurel, in a sense he is worthier of it than Leigh Hunt; only Tennyson can wait, that is the single difference.
  PASSAGE: So anxious I am about your house. Your health seems to me mainly to depend on your moving, and I do urge your moving; if not there, elsewhere.
  context after: May God bless you, ever dear friend!
I dare say you will think I have given too much importance to the rococo verses you had the goodness to speak of; but I have a horror of being disinterred, there's the truth!

[5] Anton Chekhov, Letters to His Family and Friends (1890)
  context before: If without finishing my novel I take another thousand roubles for the tour abroad, and then for living after the tour, I shall get into such a tangle that the devil himself could not pull me out by the ears. I am not in a tangle yet because I am up to all sorts of dodges, and live more frugally than a mouse; but if I go abroad everything will go to the devil.
  PASSAGE: My accounts will be in a mess and I shall get myself hopelessly in debt. The very thought of a debt of two thousand makes my heart sink.
  context after: There are other considerations, but they are all of small account beside that of money and work. And so, thoroughly digest my objections, put yourself into my skin for a moment, and decide, wouldn’t it be better for me to stay at home?

[6] John Keats, Letters to His Family and Friends (1819)
  context before: I trust it will not in the end be detrimental to you. I am going to try the Press once more, and to that end shall retire to live cheaply in the country and compose myself and verses as well as I can.
  PASSAGE: I have very good friends ready to help me--and I am the more bound to be careful of the money they lend me. It will all be well in the course of a year I hope.
  context after: I am confident of it, so do not let it trouble you at all. Mr.

[7] Charles Darwin, Life and Letters of Charles Darwin — Volume 2 (1809–1882)
  context before: Old Cader is a grand fellow, and shows himself off superbly with every changing light. We remain here till the end of July, when the H.
  PASSAGE: Wedgwoods have the house. I have been as yet in a very poor way; it seems as soon as the stimulus of mental work stops, my whole strength gives way.
  context after: As yet I have hardly crawled half a mile from the house, and then have been fearfully fatigued. It is enough to make one wish oneself quiet in a comfortable tomb."

[8] J. B. Jones, A Rebel War Clerk's Diary at the Confederate States Capital (1810–1866)
  context before: He showed me the two first words: "Dear Bledsoe." He said nothing more about resigning.
  PASSAGE: I must get more lucrative employment, or find something for my son to do. The boarding of my family, alone, comes to more than my salary; and the cost of everything is increasing.
  context after: JUNE 25TH.--More accounts of battles and massacres in Missouri and Kansas. I never thought the Yankees would be permitted to ascend the Missouri River.

[9] Raden Adjeng Kartini, Letters of a Javanese Princess (1879–1904)
  context before: I deserve a fine scolding for my long delay in writing; in large measure, it was due to indolence. I am not satisfied with myself!
  PASSAGE: What makes me so lazy and restless? I do not understand it. I am not definitely sick, but at the same time I am far from well.
  context after: I am dull, weary and uneasy; nonsense--hypochondria--there! I must seize hold of myself; it is work that I need--work that my heart is in.

[10] Ulysses S. Grant, Letters of Ulysses S. Grant to his father and his youngest sister, 1857-78 (1822–1885)
  context before: I have now been home nearly a week, but return to Springfield to-day. I have tendered my services to the Government and go to-day to make myself useful, if possible, from this until all our National difficulties are ended.
  PASSAGE: During the six days I have been at home I have felt all the time as if a duty were being neglected that was paramount to any other duty I ever owed.
  context after: I have every reason to be well satisfied with myself for the services already rendered, but to stop now would not do.
All here are well.

[11] George Sand and Gustave Flaubert, The George Sand-Gustave Flaubert Letters (1804–1876)
  context before: I see, when I am gloomy, your kind face, and I feel the radiant power of your goodness. You are a charm in the Indian summer of my sweet and pure friendships, without egoisms, and without deceptions in consequence.
  PASSAGE: Think of me sometimes, work well and call me when you are ready to loaf. If you are not ready, never mind. If your heart told you to come here, there would be feasting and joy in the family.
  context after: I saw Sainte-Beuve, I am content and proud of him.
Good night, friend of my heart.

[12] Samuel Pepys, Diary of Samuel Pepys — Volume 24: September/October 1663 (1633–1703)
  context before: So that I hope I shall not need now to lay out more money a great while, I having laid out in clothes for myself and wife, and for her closett and other things without, these two months, this and the last, besides household expenses of victuals, &c., above L110. But I hope I shall with more comfort labour to get more, and with better successe than when, for want of clothes, I was forced to sneake like a beggar.
  PASSAGE: Having done this I went home, and after supper to bed, my mind being eased in knowing my condition, though troubled to think that I have been forced to spend so much.
  context after: Thus I end this month worth L717, or thereabouts, with a good deal of good goods more than I had, and a great deal of new and good clothes. My greatest trouble and my wife's is our family, mighty out of order by this fellow Will's corrupting the mayds by his idle talke and carriage, which we are going to remove by hastening him out of the house, which his uncle Blackburne is upon doing, and I am to give him L20 per annum toward his maintenance.

[13] Mark Twain, Mark Twain's Letters — Volume 2 (1867-1875) (1835–1910)
  context before: They flood me with high-priced invitations to write for magazines and papers, and publishers besiege me to write books. Can't do any of these things.
  PASSAGE: I am twenty-two thousand dollars in debt, and shall earn the money and pay it within two years--and therefore I am not spending any money except when it is necessary.
  context after: I had my life insured for $10,000 yesterday (what ever became of Mr. Moffett' s life insurance?) “for the benefit of my natural heirs”--the same being my mother, for Livy wouldn't claim it, you may be sure of that.

[14] Marcus Tullius Cicero, Letters of Marcus Tullius Cicero (107 BC–44 BC)
  context before: There is a threat of a Parthian war. Cassius's despatch was empty brag: that of Bibulus had not arrived: when that is read I think the senate will at length be roused.
  PASSAGE: I am myself in serious anxiety. If, as I hope, my government is not prolonged, I have only June and July to fear. May it be so!
  context after: Bibulus will keep them in check for two months. What will happen to the man I leave in charge, especially if it is my brother?

[15] Abraham Lincoln, The Papers and Writings of Abraham Lincoln — Volume 5: 1858-1862 (1809–1865)
  context before: Court in your city on the 3d Tuesday of this month. I have had no thought of being there.
  PASSAGE: It is bad to be poor. I shall go to the wall for bread and meat if I neglect my business this year as well as last.
  context after: It would please me much to see the city and good people of Keokuk, but for this year it is little less than an impossibility. I am constantly receiving invitations which I am compelled to decline.

[16] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 2 (1813–1883)
  context before: I feel as if I should break down pantingly in sight of the goal. Once at least every day I look at my book with a right good will, but my head is waste, my heart empty, and I stare at the mists and the rain-clouds, which, ever since I have been here, have debarred me even from the chance of shaking up my stagnant blood by pleasant excursions.
  PASSAGE: People say: "Go to work, then all will be right." Very well in its way, but I, poor devil, lack routine, and if ideas do not come to me of themselves, I cannot make them A pleasant state of things this! and what is worse, there is no chance of helping myself in any other way.
  context after: All is shut and locked against me. Work alone is to help me, but who is to help me to the possibility of work?

[17] Robert E. Lee, Recollections and Letters of General Robert E. Lee (1843–1914)
  context before: “I am clear for your doing everything to improve your property and make it remunerative as far as you can. You know my objections to incurring debt.
  PASSAGE: I cannot overcome it.... I hope you will overcome your chills, and by next winter you must patch up your house, and get a sweet wife.
  context after: You will be more comfortable, and not so lonesome. Let her bring a cow and a churn.

[18] Horatio Nelson Nelson, The Letters of Lord Nelson to Lady Hamilton, Vol. I. With A Supplement Of Interesting Letters By Distinguished Characters (1758–1805)
  context before: I hope, the minister has done something for you. But, never mind, we can live upon bread and cheese.
  PASSAGE: Independence is a blessing; and, although I have not yet found out the way to get prize money--what has been taken, has run into our mouths--however, it must turn out very hard, if I cannot get enough to pay off my debts, and that will be no small comfort.
  context after: I have not mentioned my Bronte affairs to Acton, as yet; but, if Naples remains much longer, I shall ask the question. But, I expect nothing from them.

[19] Robert Browning and Elizabeth Barrett Browning, The letters of Robert Browning and Elizabeth Barrett Barrett, Vol. 1 (of 2) 1845-1846 (1812–1889)
  context before: Or one verse will do ... anything will do ... and don't let me be bringing you into vexation. It need not be of MS. rarity.
  PASSAGE: You are not better ... really ... I fear. And your mother's being ill affects you more than you like to admit, I fear besides.
  context after: Will you, when you write, say how both are ... nothing extenuating, you know. May God bless you, my dearest friend.

[20] Sarah Morgan Dawson, A Confederate Girl's Diary (1842–1909)
  context before: Clinton, at least, I am sure of. Lilly came down for me yesterday, and according to the present programme, though I will not answer for it in an hour from now, we leave Linwood this evening, and Clinton on Thursday.
  PASSAGE: I am almost indifferent about our destination; my chief anxiety is to have some definite plans decided on, which seems perfectly impossible from the number of times they are changed a day.
  context after: The uncertainty is really affecting my spine, and causing me to grow alarmingly thin....
```

## Case 8: Scared > Helpless > Insignificant

```
feeling: insignificant (helpless, scared)
  what happened: The doctor wants more tests.
  because: it might be something serious
  afraid it means: that I might not have much time

CANDIDATE PASSAGES
[1] Anton Chekhov, Letters to His Family and Friends (1890)
  context before: But you will never buy yourself an estate, as you don’t know what you want. To like an estate you must make up your mind to buy it; so long as it is not yours it will seem comfortless and full of defects.
  PASSAGE: My cough is considerably better, I am sunburnt, and they tell me I am fatter, but the other day I almost fell down and I fancied for a minute that I was dying.
  context after: I was walking along the avenue with the prince, our neighbour, and was talking when all at once something seemed to break in my chest, I had a feeling of warmth and suffocation, there was a singing in my ears, I remembered that I had been having palpitations for a long time and thought--“they must have meant something then.” I went rapidly towards the verandah on which visitors were sitting, and had one thought--that it would be awkward to fall down and die before strangers; but I went into my bedroom, drank some water, and recovered.
So you are not the only one who suffers from staggering!

[2] Henry Reeve, Memoirs of the Life and Correspondence of Henry Reeve, C.B., D.C.L. In Two Volumes. Volume II. (1813–1895)
  context before: St.-Hilaire
Paris, June 6th.--If I am free in the autumn, it will give me great pleasure to pay you another visit at Foxholes; the first has left a pleasant memory, and I ask no better than to repeat it.
  PASSAGE: But, without having to complain of old age, I find more difficulty in going about. I am not exactly ill, but my strength gradually fails--a sign that the end is not far off.
  context after: I foresaw that General Boulanger would have no success in England; you are much too serious for such a nature as his. His popularity diminishes daily; and if the Cabinet act with judgement from now to the October elections, I have no doubt they may regain public favour.

[3] Ludwig van Beethoven, Beethoven's Letters 1790-1826, Volume 2 (1770–1827)
  context before: I was obliged to make the effort to come here, without even being able to see Y.R.H. Thank God, my eyes are so much better that I can again venture to make tolerable use of them by daylight.
  PASSAGE: My other maladies, too, are improving, and I cannot expect more in so short a period. How I wish that Y.R.H. were only here, when in a few days we could entirely make up for lost time.
  context after: Perhaps I may still be so fortunate as to see Y.R.H. here, and be able to show my zeal to serve Y.R.H. How deeply does this cause me to lament my unhappy state of health.

[4] George Sand and Gustave Flaubert, The George Sand-Gustave Flaubert Letters (1804–1876)
  context before: In short, your Cruchard has become an intolerable old codger, because he has been intolerant. And as I cannot do anything that I ought to do, I must, out of consideration for others, spare them the overflow of my bile.
  PASSAGE: For the last six months, especially, I don't know what has been the trouble with me, but I feel dreadfully ill, without being able to get to the root of the matter, and I know many people are in the same condition.
  context after: Why? Perhaps we are suffering from the illness of France; here in Paris, where her heart beats, people feel better than at her extremities, in the provinces.

[5] Elizabeth Barrett Browning, The Letters of Elizabeth Barrett Browning (Volume 1 of 2) (1806–1861)
  context before: As to the 'Athenaeum,' although I am not conscious of the quaintness and mannerism laid to my charge, and am very sure that I have always written too naturally (that is, too much from the impulse of thought and feeling) to have studied 'attitudes,' yet the critic was quite right in stating his opinion, and so am I in being grateful to him for the liberal praise he has otherwise given me. Upon the whole, I like his review better than even the 'Examiner,' notwithstanding my being perfectly satisfied with that.
  PASSAGE: Thank you for the question about my health. I am very tolerably well--for me: and am said to look better. At the same time I am aware of being always on the verge of an increase of illness--I mean, in a very excitable state--with a pulse that flies off at a word and is only to be caught by digitalis.
  context after: But I am better--for the present--while the sun shines.
Thank you besides for your criticisms, which I shall hold in memory, and use whenever I am not particularly obstinate, in all my SUCCEEDING EDITIONS!

[6] Edward FitzGerald, Letters of Edward FitzGerald, in Two Volumes. Vol. 2 (1809–1883)
  context before: For his Niece has a Child, if only one, to attend to, and I do not like to trouble. I heard from vague Information in London that he is almost confined to his house.
  PASSAGE: I have myself been somewhat bothered at times for the last three months with pains and heaviness about the Heart: which I knew from a Doctor was unsettled five years ago.
  context after: I shall not at all complain if it takes the usual course, only wishing to avoid Angina, or some such form of the Disease. My Family get on gaily enough till seventy, and then generally founder after turning the corner.

[7] Robert Browning and Elizabeth Barrett Browning, The letters of Robert Browning and Elizabeth Barrett Barrett, Vol. 1 (of 2) 1845-1846 (1812–1889)
  context before: Or one verse will do ... anything will do ... and don't let me be bringing you into vexation. It need not be of MS. rarity.
  PASSAGE: You are not better ... really ... I fear. And your mother's being ill affects you more than you like to admit, I fear besides.
  context after: Will you, when you write, say how both are ... nothing extenuating, you know. May God bless you, my dearest friend.

[8] Charles Darwin, Life and Letters of Charles Darwin — Volume 1 (1809–1882)
  context before: I fully, also, subscribe to the proposition that it is the duty of every one to spread what he believes to be the truth; and I honour you for doing so, with so much devotion and zeal. But I cannot comply with your request for the following reasons; and excuse me for giving them in some detail, as I should be very sorry to appear in your eyes ungracious.
  PASSAGE: My health is very weak: I NEVER pass 24 hours without many hours of discomfort, when I can do nothing whatever. I have thus, also, lost two whole consecutive months this season.
  context after: Owing to this weakness, and my head being often giddy, I am unable to master new subjects requiring much thought, and can deal only with old materials. At no time am I a quick thinker or writer: whatever I have done in science has solely been by long pondering, patience and industry.

[9] Samuel Taylor Coleridge, Biographia Epistolaris, Volume 1 (1772–1834)
  context before: And I do believe that truth lies in these loose generalizations. I do not think it possible that any bodily pains could eat out the love of joy, that is so substantially part of me, towards hills, and rocks, and steep waters; and I have had some trial.
  PASSAGE: On Monday night I had an attack in my stomach and right side, which in pain, and the length of its continuance appeared to me by far the severest I ever had.
  context after: About one o'clock the pain passed out of my stomach, like lightning from a cloud, into the extremities of my right foot. My toe swelled and throbbed, and I was in a state of delicious ease, which the pain in my toe did not seem at all to interfere with.

[10] Anne Gilchrist and Walt Whitman, The Letters of Anne Gilchrist and Walt Whitman (1828–1885)
  context before: Indeed all that sympathy and warm & true words of love & sorrow & highest admiration & esteem for my darling could do to comfort me I have had--and most & best from America. And many of her poor patients at Edinburgh went sobbing from the door when they heard they should see her no more.
  PASSAGE: The report of your health is comforting dear friend. Mine too is better--I am able to take walks again--though still liable to sudden attacks of difficult breathing.
  context after: Herby is working hard--has just been disappointed over a competition design which he sent in to the Royal Academy--a very poor & specious work obtaining the premium--but is no whit discouraged & has no need to be, for he is making great progress--works hard, loves his work & is of the stuff where of great painters are made, I am persuaded--so he can afford to wait. Giddy is not quite so well & strong as I could wish, but there seems nothing serious.

[11] Robert Louis Stevenson, Vailima Letters Being Correspondence Addressed by Robert Louis Stevenson to Sidney Colvin, November 1890-October 1894 (1850–1894)
  context before: -
  PASSAGE: I am nearly dead with dyspepsia, over-smoking, and unremunerative overwork. Last night, I went to bed by seven; woke up again about ten for a minute to find myself light-headed and altogether off my legs; went to sleep again, and woke this morning fairly fit.
  context after: I have crippled on to p. 101, but I haven’t read it yet, so do not boast. What kills me is the frame of mind of one of the characters; I cannot get it through.

[12] Robert E. Lee, Recollections and Letters of General Robert E. Lee (1843–1914)
  context before: Your letters to Custis told us of your well-doing. I want to see you all very much, and think the sight of my daughter and grandson would do me good.
  PASSAGE: I have had a wretched cold, the effects of which have not left me, but I am better. The doctors still have me in hand, but I fear can do no good.
  context after: The present mild weather I hope will be beneficial, enabling me to ride and be in the open air. But Traveller’s trot is harder to me than it used to be and fatigues me.

[13] John Adams and Abigail Adams, Familiar Letters of John Adams and His Wife Abigail Adams During the Revolution with a Memoir of Mrs. Adams (1735–1826)
  context before: I cannot omit the opportunity of writing you a line by this post. This letter will, I suppose, find you, in some degree or other, under the influence of the small-pox.
  PASSAGE: The air is of very great importance. I don't know your physician, but I hope he won't deprive you of air more than is necessary.
  context after: We had yesterday an express from General Lee in Charleston, South Carolina, with an account of a brilliant little action between the armament under Clinton and Cornwallis, and a battery on Sullivan's Island, which terminated very fortunately for America. I will endeavor to inclose with this a printed account of it.

[14] Franz Liszt, Letters of Franz Liszt -- Volume 1 from Paris to Rome: Years of Travel as a Virtuoso (1811–1886)
  context before: To Countess Rosalie Sauerma, nee Spohr
Your letter gave me great pleasure, dear Countess and admirable artist, and, though still obliged to keep my bed (which I have been able to leave so little during the whole winter), I hasten to reassure you entirely about my state of health.
  PASSAGE: As a fact, I have never done my obstinate illness the honor of considering it serious, and now less than ever, for I hope to have entirely got over it by the end of the week.
  context after: So do not let us talk about it any more, and let me tell you at once how sincerely I rejoice in your projects of being, so to say, in the neighborhood of Dresden, for it seems to me that, among the towns of Germany, it is the one in which you will find most charm. I shall certainly come and pay you my visit there in the course of the winter, and I hope also that you will not altogether forget your friends of Weymar.

[15] Jonathan Swift, The Journal to Stella (1667–1745)
  context before: He would never let me look at his watch, and I could not imagine it above twelve when we went away. So I bid you good-night for last night, and now I bid you good-morrow, and I am still in bed, though it be near ten, but I must rise.
  PASSAGE: 26, 27, 28, 29, 30. I have been so lazy and negligent these last four days that I could not write to MD. My head is not in order, and yet is not absolutely ill, but giddyish, and makes me listless; I walk every day, and take drops of Dr.
  context after: Cockburn, and I have just done a box of pills; and to-day Lady Kerry sent me some of her bitter drink, which I design to take twice a day, and hope I shall grow better. I wish I were with MD; I long for spring and good weather, and then I will come over.

[16] Victoria, Queen of Great Britain, The letters of Queen Victoria, vol. 3, 1854-1861 (1819–1901)
  context before: MY BELOVED UNCLE,--I enclose you Clark's report, which I think you may like to hear. Our beloved invalid goes on well--but it must be tedious, and I need not tell you what a trial it is to me.
  PASSAGE: Every day, however, is bringing us nearer the end of this tiresome illness, which is much what I had at Ramsgate, only that I was much worse, and not at first well attended to.
  context after: You shall hear daily.
You will, I know, feel for me!

[17] Raden Adjeng Kartini, Letters of a Javanese Princess (1879–1904)
  context before: I deserve a fine scolding for my long delay in writing; in large measure, it was due to indolence. I am not satisfied with myself!
  PASSAGE: What makes me so lazy and restless? I do not understand it. I am not definitely sick, but at the same time I am far from well.
  context after: I am dull, weary and uneasy; nonsense--hypochondria--there! I must seize hold of myself; it is work that I need--work that my heart is in.

[18] John Keats, Letters to His Family and Friends (1819)
  context before: My dear Rice--I have not been well enough to make any tolerable rejoinder to your kind letter. I will, as you advise, be very chary of my health and spirits.
  PASSAGE: I am sorry to hear of your relapse and hypochondriac symptoms attending it. Let us hope for the best, as you say. I shall follow your example in looking to the future good rather than brooding upon the present ill.
  context after: I have not been so worn with lengthened illnesses as you have, therefore cannot answer you on your own ground with respect to those haunting and deformed thoughts and feelings you speak of. When I have been, or supposed myself in health, I have had my share of them, especially within the last year.

[19] Fanny Kemble, Journal of a Residence on a Georgian Plantation: 1838-1839 (1809–1893)
  context before: Friday, March 1.--Last night after writing so much to you I felt weary, and went out into the air to refresh my spirit. The scene just beyond the house was beautiful, the moonlight slept on the broad river which here is almost the sea, and on the masses of foliage of the great southern oaks; the golden stars of German poetry shone in the purple curtains of the night, and the measured rush of the Atlantic unfurling its huge skirts upon the white sands of the beach (the sweetest and most awful lullaby in nature) resounded through the silent air.
  PASSAGE: I have not felt well, and have been much depressed for some days past. I think I should die if I had to live here.
  context after: This morning, in order not to die yet, I thought I had better take a ride, and accordingly mounted the horse which I told you was one of the equestrian alternatives offered me here; but no sooner did he feel my weight, which, after all, is mere levity and frivolity to him, than he thought proper to rebel, and find the grasshopper a burthen, and rear and otherwise demonstrate his disgust. I have not ridden for a long time now, but Montreal's opposition very presently aroused the Amazon which is both natural and acquired in me, and I made him comprehend that, though I object to slaves, I expect obedient servants; which views of mine being imparted by a due administration of both spur and whip, attended with a judicious combination of coaxing pats on his great crested neck, and endearing commendations of his beauty, produced the desired effect.

[20] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 2 (1813–1883)
  context before: I had foreseen all this, and therefore during Tichatschek's stay of twelve days, was in a state of continual, painful anxiety. This abominable illness has brought me very low.
  PASSAGE: In the month of May alone I had three relapses, and even now not an hour passes without my living in fear of a new attack.
  context after: In consequence, I am unfit for anything, and it is obvious that I must think of my thorough recovery. For that purpose a painfully strict regime with regard to diet and general mode of life is required; the slightest disorder of my stomach immediately affects my complaint.
```

## Case 9: Mad > Selfish > Jealous

```
feeling: jealous (selfish, mad)
  what happened: Everyone I know is getting promoted or engaged.
  because: I am stuck where I was
  afraid it means: that I am falling behind for good

CANDIDATE PASSAGES
[1] Mark Twain, Mark Twain's Letters — Volume 4 (1886-1900) (1835–1910)
  context before: DEAR HOWELLS,--I find your generous article in the Weekly, and I want to thank you for its splendid praises, so daringly uttered and so warmly. The words stir the dead heart of me, and throw a glow of color into a life which sometimes seems to have grown wholly wan.
  PASSAGE: I don't mean that I am miserable; no--worse than that--indifferent. Indifferent to nearly everything but work. I like that; I enjoy it, and stick to it.
  context after: I do it without purpose and without ambition; merely for the love of it.
This mood will pass, some day--there is history for it.

[2] Louis Agassiz, Louis Agassiz: His Life and Correspondence (1807–1873)
  context before: It is a great pleasure to have at least a part of our Swiss mountains always in sight. To enjoy it the more, I have placed my table opposite the window, so that every time I lift my head my eyes rest on our dear country.
  PASSAGE: This does not prevent me from feeling dull sometimes, especially when I am alone, but I hope this will pass off when my occupations become more regular. . .
  context after: A far more stimulating intellectual life than that of Heidelberg awaited our students at Munich. Among their professors were some of the most original men of the day,--men whose influence was felt all over Europe.

[3] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 2 (1813–1883)
  context before: Cordial thanks for your New Year's greeting, dearest Richard. I expect to see the explanation of the last words of your telegram in your next letter, for I have no knowledge of the event which you describe as "wonderfully miserable."
  PASSAGE: In certain quarters, however, the MISERABLE appears no longer WONDERFUL to me. I hope the new year will bring some things to a better issue, and have many good things in store for you.
  context after: Enclosed I send you this week's repertoire of the Weymar theatre, in which you will see the announcement of "Lohengrin" for next Sunday. For the first time I shall not conduct this work to which I am attached with my whole soul.

[4] George Sand and Gustave Flaubert, The George Sand-Gustave Flaubert Letters (1804–1876)
  context before: I teach my servant to read, I correct proof and I am well. That is my life and nothing bores me in this world where I think that AS FAR AS I AM CONCERNED all is for the best.
  PASSAGE: But I am afraid of becoming more of a bore than I used to be. People don't like such as I am very much. We are too inoffensive.
  context after: However, love me still a little, for I feel by the disappointment of not seeing you, that it would have gone hard with me if you had meant to break your word.
And I embrace you tenderly, dear old friend.

[5] Henri Frédéric Amiel, Amiel's Journal: The Journal Intime of Henri-Frédéric Amiel (1821–1881)
  context before: (Hyères.)--In spite of my sleeping draught I have had a bad night. Once it seemed as if I must choke, for I could breathe neither way.
  PASSAGE: Could I be more fragile, more sensitive, more vulnerable! People talk to me as if there were still a career before me, while all the time I know that the ground is slipping from under me, and that the defense of my health is already a hopeless task.
  context after: At bottom, I am only living on out of complaisance and without a shadow of self-delusion. I know that not one of my desires will be realized, and for a long time I have had no desires at all.

[6] Anne Gilchrist and Walt Whitman, The Letters of Anne Gilchrist and Walt Whitman (1828–1885)
  context before: If you could look into my spirit & emotion you would be entirely satisfied & at peace. I am at present temporarily here at Camden, on the Delaware river, opposite Philadelphia, at the house of my brother, and I am occupying, as I write, the rooms wherein my mother died.
  PASSAGE: You must not be unhappy about me, as I am as comfortably situated as can be--& many things--indeed every thing--in my case might be so much worse.
  context after: Though my plans are not definite, my intention as far as anything is on getting stronger, and after the hot season passes, to get back to Washington for the fall & winter.
My post office address continues at Washington.

[7] Elizabeth Barrett Browning, The Letters of Elizabeth Barrett Browning (Volume 2 of 2) (1806–1861)
  context before: She failed in it, I am sorry to say--it did not 'draw,' as the phrase is. Now she has left Paris, but is likely to return.
  PASSAGE: I am sure it will do you great good to have change and liberty and distraction in various ways. The 'anxiety' you speak of--oh, I do hope it does not relate to Gerardine.
  context after: I always think of her when you seem anxious.
I shall be very glad if, when you come, you should be inclined to give your attention, you with your honest and vigorous mind, to the facts of the political situation, not the facts as you hear them from the English, or from our friend Madme Mohl, who confessed to me one day that she liked exaggerations because she hated the President.

[8] Anton Chekhov, Letters to His Family and Friends (1890)
  context before: I am afraid that in this respect I resemble Gontcharov, whom I don’t like, who is ten heads taller than I am in talent. I have not enough passion; add to that this sort of lunacy: for the last two years I have for no reason at all ceased to care about seeing my work in print, have become indifferent to reviews, to literary conversations, to gossip, to success and failure, to good pay--in short, I have gone downright silly.
  PASSAGE: There is a sort of stagnation in my soul. I explain it by the stagnation in my personal life. I am not disappointed, I am not tired, I am not depressed, but simply everything has suddenly become less interesting.
  context after: I must do something to rouse myself.

[9] Amy Fay, Music-Study in Germany, from the Home Correspondence of Amy Fay (1844–1928)
  context before: I find that the strengthening and equalizing of the fingers is a terribly slow process, and that it takes much more time to make a step forward than I expected. You may know how a thing ought to be played, but it is another matter to get your hands into such a training that they obey your will.
  PASSAGE: Sometimes I am very much encouraged, and feel as if I should be an artist "immediately, if not sooner," and at others I fall into the blackest despair.
  context after: I don't know but that S. J. was in the right of it, not to attempt anything, for it is an awful pull when you do once begin to study!

[10] Robert Louis Stevenson, The Works of Robert Louis Stevenson - Swanston Edition, Vol. 23 (1850–1894)
  context before: -
  PASSAGE: At times I get terribly frightened about my work, which seems to advance too slowly. I hope soon to have a greater burden to support, and must make money a great deal quicker than I used.
  context after: I may get nothing for the Vendetta; I may only get some forty quid for the Emigrant; I cannot hope to have them both done much before the end of November.
O, and look here, why did you not send me the Spectator which slanged me?

[11] Thomas Carlyle and Ralph Waldo Emerson, The Correspondence of Thomas Carlyle and Ralph Waldo Emerson, 1834-1872, Vol. I (1795–1881)
  context before: In these four years, so full of pain and toil, I seem to have lived four decades. By degrees, the creature gets accustomed to its element; the salamander learns to live in fire, and be of the same temperature with it.
  PASSAGE: Ah me! I feel as if grown old innumerable things are become weary, flat, stale, and unprofitable. And yet perhaps I am not old, only wearied, and there is a stroke or two of work in me yet.
  context after: For the rest, the fret and agitation of this Babylon wears me down: it is the most unspeakable life; of sunbeams and miry clay; a contradiction which no head can reconcile. Pain and poverty are not wholesome; but praise and flattery along with them are poison: God deliver us from that; it carries madness in the very breath of it!

[12] Samuel Pepys, Diary of Samuel Pepys — Volume 22: May/June 1663 (1633–1703)
  context before: Coventry; for which I am sorry. The King of France was given out to be poisoned and dead; but it proves to be the measles: and he is well, or likely to be soon well again.
  PASSAGE: I find myself growing in the esteem and credit that I have in the office, and I hope falling to my business again will confirm me in it, and the saving of money which God grant!
  context after: So to supper, prayers, and bed. My whole family lying longer this morning than was fit, and besides Will having neglected to brush my clothes, as he ought to do, till I was ready to go to church, and not then till I bade him, I was very angry, and seeing him make little matter of it, but seeming to make it a matter indifferent whether he did it or no, I did give him a box on the ear, and had it been another day should have done more.

[13] Arthur Christopher Benson, The Upton Letters (1862–1925)
  context before: You will be able, too, to live a more undisturbed life, not fretted by all the cross-currents which distract a man in his own land, when he has a large variety of ties. I declare I did not know I was so good a rhetorician; I shall end by convincing myself that there is no real happiness to be found except in expatriation!
  PASSAGE: Seriously, my dear Herbert, I do understand the sadness of the change; but one gets no good by dwelling on the darker side; there are and will be times, I know, of depression.
  context after: When one lies awake in the morning, before the nerves are braced by contact with the wholesome day; when one has done a tiring piece of work, and is alone, and in that frame of mind when one needs occupation but yet is not brisk enough to turn to the work one loves; in those dreary intervals between one's work, when one is off with the old and not yet on with the new--well I know all the corners of the road, the shadowy cavernous places where the demons lie in wait for one, as they do for the wayfarer (do you remember?), in Bewick, who, desiring to rest by the roadside, finds the dingle all alive with ambushed fiends, horned and heavy-limbed, swollen with the oppressive clumsiness of nightmare. But you are not inexperienced or weak.

[14] Dorothy Osborne, The Love Letters of Dorothy Osborne to Sir William Temple, 1652-54 (1627–1695)
  context before: If I can keep her to Michaelmas I may perhaps bring her up to town myself, and take that occasion of seeing you; but I have no other business that is worth my taking a journey, for I have had another summons from my aunt, and I protest I am afraid I shall be in rebellion there; but 'tis not to be helped. The widow writes me word, too, that I must expect her here about a month hence; and I find that I shall want no company, but only that which I would have, and for which I could willingly spare all the rest.
  PASSAGE: Will it be ever thus? I am afraid it will. There has been complaints made on me already to my eldest brother (only in general, or at least he takes notice of no more), what offers I refuse, and what a strange humour has possessed me of being deaf to the advice of all my friends.
  context after: I find I am to be baited by them all by turns. They weary themselves, and me too, to very little purpose, for to my thinking they talk the most impertinently that ever people did; and I believe they are not in my debt, but think the same of me.

[15] Ambrose Bierce, The Letters of Ambrose Bierce, With a Memoir by George Sterling (1842–1914)
  context before: It's a long time since the date of your latest letter, but I've been doing two men's work for many weeks and have actually not found the leisure to write to my friends.
  PASSAGE: As it is the first time that I've worked really hard for several years I ought not to complain, and don't. But I hope it will end with this session of Congress.
  context after: I think I did not thank you for the additional copies of your new book--the new edition. I wish it contained the new poem, "A Wine of Wizardry."

[16] Robert Browning and Elizabeth Barrett Browning, The letters of Robert Browning and Elizabeth Barrett Barrett, Vol. 1 (of 2) 1845-1846 (1812–1889)
  context before: What should make you, dearest friend, weary in your soul; or out of spirits in any way?--Do ... tell me.... I was going to write without a pause--and almost I might, perhaps, ... even as one of the two hundred of your friends, ... almost I might say out that 'Do tell me.'
  PASSAGE: Or is it (which I am inclined to think most probable) that you are tired of a same life and want change? It may happen to anyone sometimes, and is independent of your will and choice, you know--and I know, and the whole world knows: and would it not therefore be wise of you, in that case, to fold your life new again and go abroad at once?
  context after: What can make you weary in your soul, is a problem to me. You are the last from whom I should have expected such a word.

[17] Nathaniel Hawthorne, Passages from the English Notebooks, Volume 1. (1804–1864)
  context before: My early life was perhaps a good preparation for the declining half of life; it having been such a blank that any thereafter would compare favorably with it. For a long, long while, I have occasionally been visited with a singular dream; and I have an impression that I have dreamed it ever since I have been in England.
  PASSAGE: It is, that I am still at college,--or, sometimes, even at school,--and there is a sense that I have been there unconscionably long, and have quite failed to make such progress as my contemporaries have done; and I seem to meet some of them with a feeling of shame and depression that broods over me as I think of it, even when awake.
  context after: This dream, recurring all through these twenty or thirty years, must be one of the effects of that heavy seclusion in which I shut myself up for twelve years after leaving college, when everybody moved onward, and left me behind. How strange that it should come now, when I may call myself famous and prosperous!--when I am happy, too!

[18] Walter Scott, The Journal of Sir Walter Scott From the Original Manuscript at Abbotsford (1771–1832)
  context before: I can answer conscientiously, I do. The love of solitude was with me a passion of early youth; when in my teens, I used to fly from company to indulge in visions and airy castles of my own, the disposal of ideal wealth, and the exercise of imaginary power.
  PASSAGE: This feeling prevailed even till I was eighteen, when love and ambition awakening with other passions threw me more into society, from which I have, however, at times withdrawn myself, and have been always even glad to do so.
  context after: I have risen from a feast satiated; and unless it be one or two persons of very strong intellect, or whose spirits and good-humour amuse me, I wish neither to see the high, the low, nor the middling class of society. This is a feeling without the least tinge of misanthropy, which I always consider as a kind of blasphemy of a shocking description.

[19] of Siena Catherine, Letters of Catherine Benincasa (1347–1380)
  context before: He turned as does the Bride when she has reached the threshold of her bridegroom, who turns back her head and her look, bowing to those who have accompanied her, and with the gesture she gives signs of thanks.
When he was at rest, my soul rested in peace and in quiet, in so great fragrance of blood that I could not bear to remove the blood which had fallen on me from him.
  PASSAGE: Ah me, miserable! I will say no more. I stayed on the earth with the greatest envy. And it seems to me that the first new stone is already in place.
  context after: Therefore do not wonder if I impose upon you nothing save to see yourselves drowned in the blood and flame poured from the side of the Son of God. Now then, no more negligence, sweetest my sons, since the blood is beginning to flow, and to receive the life.

[20] S. R. Crockett, Sweethearts at Home (1860–1914)
  context before: And when her birthday came round Uncle Tom chose for her present--a pipe-rack for the smoking-room!
I think that was fine--and so does Hugh John.
  PASSAGE: Now I am not complaining. August the tenth is my birthday, and it is a good time for birthdays--being sufficiently long before Christmas. I pity the poor people who were born in early January.
  context after: Also presents are good at our house, and there are enough of us to change round among ourselves if any mistakes do occur. But what I really want to tell you about is what happened to Little Sarah Brown, who lives just outside our gate.
```

## Case 10: Sad > Lonely > Isolated

```
feeling: isolated (lonely, sad)
  what happened: My best friend moved to another city and stopped answering my messages.
  because: I think I did something wrong
  afraid it means: that I am easy to leave

CANDIDATE PASSAGES
[1] Henri Frédéric Amiel, Amiel's Journal: The Journal Intime of Henri-Frédéric Amiel (1821–1881)
  context before: July 21, 1856.--Mit sack und pack here I am back again in my town rooms. I have said good-bye to my friends and my country joys, to verdure, flowers, and happiness.
  PASSAGE: Why did I leave them after all? The reason I gave myself was that I was anxious about my poor uncle, who is ill. But at bottom are there not other reasons?
  context after: Yes, several. There is the fear of making myself a burden upon the two or three families of friends who show me incessant kindness, for which I can make no return.

[2] Richard Wagner and Franz Liszt, Correspondence of Wagner and Liszt — Volume 1 (1813–1883)
  context before: I can get no real information from there. It is very long since I heard anything of you!
  PASSAGE: Alas! I am out of sorts and God-forsaken. I feel so lonely, and yet do not want to see any one. What a miserable existence!
  context after: I cannot help smiling when I read in B.'s paper the articles by R. F.'s brother-in-law; the man thinks he is going thoroughly to the bottom of the thing, because he is so moderate and cautious; he knows very little of me.

[3] Sarah Morgan Dawson, A Confederate Girl's Diary (1842–1909)
  context before: Miriam says mother is looking very sad. Sad, and I am trying to forget all our troubles, and am so happy here!
  PASSAGE: O mother, how selfish it was to leave you! I ask myself whether it were best to stay there where we would only be miserable without adding anything to your comfort or pleasure, or to be here, careless and happy while you are in that horrid hole so sad and lonesome.
  context after: According to my theory, Miriam would remind me that I say it is better to have three miserable persons than two happy ones whose happiness occasions the misery of the third. That is my doctrine only in peculiar cases; it cannot be applied to this one.

[4] Arthur Christopher Benson, The Upton Letters (1862–1925)
  context before: But I am here, a lonely man, wondering and doubting and desiring I hardly know what. Some nearness of life, some children of my own.
  PASSAGE: You are apt to think of yourself as shelved and isolated; yet, after all, you have the real thing--wife, children, and home. But, in my case, these boys who are dear to me have forgotten me already.
  context after: Disguise it as I will, I am part of the sordid furniture of life that they have so gladly left behind, the crowded corridor, the bare-walled schoolroom, the ink-stained desk. They are glad to think that they have not to assemble to-morrow to listen to my prosing, to bear the blows of the uncle's tongue, as Horace says.

[5] Charles Lamb and Mary Lamb, The Works of Charles and Mary Lamb — Volume 5 The Letters of Charles and Mary Lamb, 1796-1820 (1775–1834)
  context before: My brother is gone to Paris.
Dear Miss H.--I am forced to be the replier to your Letter, for Mary has been ill and gone from home these five weeks yesterday.
  PASSAGE: She has left me very lonely and very miserable. I stroll about, but there is no rest but at one's own fireside, and there is no rest for me there now.
  context after: I look forward to the worse half being past, and keep up as well as I can. She has begun to show some favorable symptoms.

[6] Byron, George Gordon Byron, The Works of Lord Byron: Letters and Journals. Vol. 2 (1788–1824)
  context before: My Dear Sir,--I am indeed "in your debt,"--and, what is still worse, am obliged to follow royal example (he has just apprised his creditors that they must wait till the next meeting), and intreat your indulgence for, I hope, a very short time.
  PASSAGE: The nearest relation and almost the only friend I possess, has been in London for a week, and leaves it tomorrow with me for her own residence.
  context after: I return immediately; but we meet so seldom, and are so minuted when we meet at all, that I give up all engagements till now, without reluctance. On my return, I must see you to console myself for my past disappointment.

[7] William Hazlitt, Liber Amoris, Or, The New Pygmalion (1778–1830)
  context before: The agony, the conflict of hope and fear, of adoration and jealousy is over; or it would, ere long, have ended with my life. I am no more lifted now to Heaven, and then plunged in the abyss; but I seem to have been thrown from the top of a precipice, and to lie groveling, stunned, and stupefied.
  PASSAGE: I am melancholy, lonesome, and weaker than a child. The worst is, I have no prospect of any alteration for the better: she has cut off all possibility of a reconcilement at any future period.
  context after: Were she even to return to her former pretended fondness and endearments, I could have no pleasure, no confidence in them. I can scarce make out the contradiction to myself.

[8] John Adams and Abigail Adams, Familiar Letters of John Adams and His Wife Abigail Adams During the Revolution with a Memoir of Mrs. Adams (1735–1826)
  context before: We have had four of the coldest days I ever knew, and they were followed by the severest snow-storm I ever remember. The wind, blowing like a hurricane for fifteen or twenty hours, rendered it impossible for man or beast to live abroad, and has blocked up the roads so that they are impassable.
  PASSAGE: A week ago I parted with my daughter, at the request of our Plymouth friends, to spend a month with them; so that I am solitary indeed.
  context after: Can the best of friends recollect that for fourteen years past I have not spent a whole winter alone? Some part of the dismal season has heretofore been mitigated and softened by the social converse and participation of the friend of my youth.

[9] Horace Walpole, The Letters of Horace Walpole, Earl of Orford — Volume 1 (1717–1797)
  context before: I have always flung it away all in the most idle manner; but, my dear Harry, idle -,is I am, and thoughtless, I have sense enough to have real pleasure in denying myself baubles, and in saving a very good income to make a man happy, for whom I have a just esteem and most sincere friendship. I know the difficulties any gentleman and man of spirit must struggle with, even in having such an offer made him, much more in accepting it.
  PASSAGE: I hope you will allow there are some in making it. But hear me: if there is such a thing as friendship in the world, these are the opportunities of exerting it, and it can't be exerted without it is accepted.
  context after: I must talk of myself to prove to you that it will be right for 'you to accept it. I am sensible of having more follies and weaknesses, and fewer real good qualities than most men.

[10] Roe, Frances Marie Antoinette Mack, Army Letters from an Officer's Wife, 1871-1888 (?–1920)
  context before: Major Pierce was promoted to another regiment and we miss them very much.
FORT SHAW, MONTANA TERRITORY, July, 1882.
  PASSAGE: THE garrison seems lonesome since the two companies have been out, and I am beginning to feel that I am at home alone quite too much.
  context after: Faye was in Washington two months, and almost immediately after he got back he was ordered to command the paymaster's escort from Helena here, and now he is off again for the summer! The camp is on Birch Creek not far from the Piegan Agency.

[11] Mary Wollstonecraft, Posthumous Works of the Author of A Vindication of the Rights of Woman (1759–1797)
  context before: Had you written one haphazard, it would have been kind and considerate--you might have known, had you thought, that the wind would not permit me to depart. These are attentions, more grateful to the heart than offers of service--But why do I foolishly continue to look for them?
  PASSAGE: Adieu! adieu! My friend--your friendship is very cold--you see I am hurt.--God bless you! I may perhaps be, some time or other, independent in every sense of the word--Ah! there is but one sense of it of consequence.
  context after: I will break or bend this weak heart--yet even now it is full.

[12] George Sand and Gustave Flaubert, The George Sand-Gustave Flaubert Letters (1804–1876)
  context before: Are you at Croisset? You must have been in Paris for the funeral of this poor friend.
  PASSAGE: What cruel and repeated separations! I am angry with you for becoming savage and discontented with life. It seems to me that you regard happiness too much as a possible thing, and that the absence of happiness which is our chronic state, angers you and astonishes you too much.
  context after: You shun friends, you plunge into work, and reckon ass lost the time you might employ in loving or in being loved. Why didn't you come to us with Madame Viardot and Tourgueneff?

[13] Forbes Robinson, Letters to His Friends (1867–1904)
  context before: I tell you what has been the greatest possible strength to me of late. God is not merely a Person, He is Three Persons in One.
  PASSAGE: I am always trying to get closer to those whom I love best, to know them more, to serve them better. Yet something is ever keeping us apart.
  context after: I said 'something,' I mean 'some one,' for only a person can keep a person from another--only a malicious, a devilish person--yet I feel that some day I shall be able to love, and know them better. Then I look out on life and I see how again and again death, and some one worse than death, is separating us, misinterpreting motives, keeping men apart; men are struggling to be one, and cannot be; on earth persons long to be one, persons who love feel they ought to be, they must be one.

[14] Napoleon I, Emperor of the French, Napoleon's Letters to Josephine, 1796-1812 For the First Time Collected and Translated, with Notes Social, Historical, and Chronological, from Contemporary Sources (1769–1821)
  context before: You have shown courage; it is necessary that you should maintain it and not give way to a doleful melancholy. You must be contented and take special care of your health, which is so precious to me.
  PASSAGE: If you are attached to me and if you love me, you should show strength of mind and force yourself to be happy. You cannot question my constant and tender friendship, and you would know very imperfectly all the affection I have for you if you imagined that I can be happy if you are unhappy, and contented if you are ill at ease.
  context after: Adieu, dear. Sleep well; dream that I wish it.

[15] John Keats, Letters to His Family and Friends (1819)
  context before: You would scarcely imagine I could live alone so comfortably. "Kepen in solitarinesse."
  PASSAGE: I told Anne, the servant here, the other day, to say I was not at home if any one should call. I am not certain how I should endure loneliness and bad weather together.
  context after: Now the time is beautiful. I take a walk every day for an hour before dinner, and this is generally my walk: I go out the back gate, across one street into the cathedral yard, which is always interesting; there I pass under the trees along a paved path, pass the beautiful front of the cathedral, turn to the left under a stone doorway,--then I am on the other side of the building,--which leaving behind me, I pass on through two college-like squares, seemingly built for the dwelling-place of deans and prebendaries, garnished with grass and shaded with trees; then I pass through one of the old city gates, and then you are in one college street, through which I pass, and at the end thereof crossing some meadows, and at last a country alley of gardens, I arrive, that is my worship arrives, at the foundation of St.

[16] Anton Chekhov, Letters to His Family and Friends (1890)
  context before: In comparison with all the “jeunes Siberiennes” with their Yakut-Buriat physiognomies, who do not know how to dress, to sing, and to laugh, our Jamais, Drishka, and Gundassiha are simply queens. The Siberian girls and women are like frozen fish; one would have to be a walrus or a seal to get up a flirtation with them.
  PASSAGE: I am tired of my companions. It is much nicer travelling alone. I like silence better than anything on the journey and my companions talk and sing without stopping, and they talk of nothing but women.
  context after: They borrowed a hundred and thirty-six roubles from me till to-morrow and have already spent it. They are regular sieves.

[17] Charles Lever, Charles Lever, His Life in His Letters, Vol. II (1806–1872)
  context before: “A Mr Crane, West George Street, Glasgow, writes me a very courteous note, and says, ‘I do thank the Editor of “Blackwood” for publishing what you say of Scott,’ and goes on to express his hearty concurrence with it all, and he regrets that it had not been spoken instead of written, &c, &c.
“I do not feel as if I was to get better this time; but I have called wolf so often I shall scream no more.
  PASSAGE: What I feel most, and struggle against most in vain, is depression. I have got to believe not only that my brains are leaving me, but that my friends are tired of me.
  context after: Of course, I couple the two disasters together, and long to be beyond the reach of remembering either one or the other.
“You read my MS. so easily that if you do not like the O’D. don’t print it--it saves me a disappointment at least; and above all, do not mind any chance irritability I display in writing, for a cry escapes me in my pain, and I often do not hear it myself.

[18] Walter Scott, The Journal of Sir Walter Scott From the Original Manuscript at Abbotsford (1771–1832)
  context before: February 12.--Having ended the second volume of Woodstock last night, I have to begin the third this morning. Now I have not the slightest idea how the story is to be wound up to a catastrophe.
  PASSAGE: I am just in the same case as I used to be when I lost myself in former days in some country to which I was a stranger.
  context after: I always pushed for the pleasantest road, and either found or made it the nearest. It is the same in writing, I never could lay down a plan--or, having laid it down, I never could adhere to it; the action of composition always diluted some passages, and abridged or omitted others; and personages were rendered important or insignificant, not according to their agency in the original conception of the plan, but according to the success, or otherwise, with which I was able to bring them out.

[19] Robert Browning and Elizabeth Barrett Browning, The letters of Robert Browning and Elizabeth Barrett Barrett, Vol. 1 (of 2) 1845-1846 (1812–1889)
  context before: What should make you, dearest friend, weary in your soul; or out of spirits in any way?--Do ... tell me.... I was going to write without a pause--and almost I might, perhaps, ... even as one of the two hundred of your friends, ... almost I might say out that 'Do tell me.'
  PASSAGE: Or is it (which I am inclined to think most probable) that you are tired of a same life and want change? It may happen to anyone sometimes, and is independent of your will and choice, you know--and I know, and the whole world knows: and would it not therefore be wise of you, in that case, to fold your life new again and go abroad at once?
  context after: What can make you weary in your soul, is a problem to me. You are the last from whom I should have expected such a word.

[20] Robert E. Lee, Recollections and Letters of General Robert E. Lee (1843–1914)
  context before: “My Dear Fitzhugh:...I hope that you are all well and that you will not let any one spoil my grandson. Your mother has written all the family and Lexington news.
  PASSAGE: She gathers much more than I do. I go nowhere but to the college, and when the weather permits I ride in the mountains. I am better, I think, but still troubled.
  context after: Mildred, I hope, is with you. When she gets away from her papa, she does not know what she wants to do, tell her.
```
