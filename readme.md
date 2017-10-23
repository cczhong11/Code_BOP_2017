# Beauty of Programming 2017

## Qualification round question

[link](https://studentclub.msra.cn/bop2017/rules/qualification)

We need to design a document based question answering system. In the dataset, one article is splited into several sentences and only one is the right answer to the questions. The datasets looks like this:

>When did Obama serve in the U.S. Senate?    Barack Obama II born August 4, 1961) is an American politician who served as the 44th President of the United States from 2009 to 2017. <br>
>When did Obama serve in the U.S. Senate?    He is the first African American to have served as president.<br> 
>When did Obama serve in the U.S. Senate?    He previously served in the U.S. Senate representing Illinois from 2005 to 2008 and in the Illinois State Senate from 1997 to 2004.<br>

## Code explanation

### Idea
1. Reading all datasets and giving each question a tag based on the keyword in the questions. I built 6 tags to all questions: time, number, entity, location, description, other. 
1. Using jieba library to separate question and sentences into words. 
1. Scoring each sentences based on the similarities between keywords in questions and answers.
1. Modifying scores based on different tags of questions.


### Code
1. `main.py` Reading datasets and save each questions and answers in `Ques` object.
1. `Ques.py` Defining Ques class and calculate different types scores.