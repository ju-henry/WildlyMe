# WildlyMe

## WildlyMe is an AI-based personality test. 
### Answer 10 questions and you'll know which animal you are!

Here it is: [https://wildlyme.streamlit.app/](https://wildlyme.streamlit.app/)

(WildlyMe is still under development.)

<div class="justified">

## How it works

WildlyMe uses sentence embeddings and semantic similarities to find the best matching animal based on ten answers.
The user experience is similar to the one of traditional personality tests; only the underlying scoring mechanism changes. This said, all questions and information on animals were generated through few-shot learning.

## Main challenges and objectives

Not using a human-made scoring of each answer and animal has one advantage: no specialized knowledge on animals is required as embeddings should implicitly encode it. The downside is that there is no control over how an answer contributes to the final scoring. 
Indeed, embeddings work similarly to a black box and this must be overcome to some extent. 
With this in mind, let us define a "good" behaviour of a personality test by giving some criteria:

1. the pairing of answers and animals is plausible, i.e. it does not contradict common knowledge on animals, e.g. if a user answers that he dislikes hierarchy, he should not be matched with a lion. 
2. the test is not a priori biased, i.e. the probability distribution over all animals of all possible combinations of answers is even.
3. (optional) the end result is clear-cut, i.e. the distance between the first and second best-matching animals is as large as possible.

## Main directions / ideas

To better specify the problem, we use a fixed set of target animals. As already mentioned, 10 questions are to be answered.
These questions are the main variables: we can make, assess, sort and discard them. Potentially, we can have a pool of more than 10 questions, from which to choose from for each user. Here are a few lines of exploration:

- Embedding each answer separately and summing the embeddings of the 10 chosen answers can be a way to assess the effect of each answer. It also makes the results independent from the order of the questions.
- Comparing results using different sets of embeddings (e.g. from BERT, from Mistral) can be done as well.
- To achieve objective 2., we can have a pool of more than 10 questions and try to find the best subset, i.e. the one whose probability distribution is the most even. 
- Producing questions can be done using few-shot learning. Then we can have criteria to include the questions in the pool, e.g. we may want to impose that answers have relatively different effects w.r.t. the target, we may also want that questions are relatively different from one another.
- If we produce new questions, we should be able to include them or not based on some criteria, then find the best subet of questions so that the test is not biased, all this in an iterative fashion to see the quality criteria improve.

WORK IN PROGRESS.

## Sources

- [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://aclanthology.org/N19-1423) (Devlin et al., NAACL 2019)  

- [https://www.animalinyou.com/](https://www.animalinyou.com/)