# Part 1: Part-of-Speech Tagging

### Objective:
Predict the parts of speech for each word in the given sentence using the probability models - Simple, Viterbi(HMM) and Markov Chain Monte Carlo(MCMC).

### Formulation of each problem:

##### Training the dataset - 
To get the probabilities for the word and their parts of speech in the required formats for implementing the probabilistic models, the following four dictionaries are created -

emi_ident    - Contains the overall probabilities of the different parts of speech

word_list    - Contains the words of the train file as the keys and each word has a dictionary of probabilities of different parts of speech for that word -> P(Word/POS)

trans_ident  - It has the transition probabilities of the parts of speech to the next part of speech occuring in the sentence

trans_ident2 - It has the transition probabilities of the parts of speech to the two consecutive parts of speech occuring in the sentence


##### Defining Simple Probability model -
In the simple model, for each word in the sentence the values -> (emission probability of word and part-of-speech) * (Overall probability of part-of-speech) is compared and the part-of-speech having the max value is returned.
Since there are some words in the test file which are not there in the trained set, the part-of-speech having the maximum overall probability is returned.

##### Defining Viterbi(HMM) Proboability model - 
In the Viterbi model, two initial dictionaries having all parts of speech as their keys with their values being list of n zeros where n is the number of words in the sentence.

The two initial dictionaries are -

hmm : Having the max probability value 

pos : Having the part-of-speech having the max probability value

The hmm dictionary first word values are then updated with P(POS)*P(Word/POS).
After this, we loop through the sentence from the second word and the second loop for all the part-of-speech. In these loops, the max probability value is found under each by calculating their transitions and hmm and pos dictionaries are updated.
Upon updating the dictionaries, we start backtracking. The max probability value and the corresponding part-of-speech is found for the last word. Using the pos dictionary, we then backtrack and iteratively update the predicted part-of-speech for each word which is then returned as output.

##### Defining Monte Carlo Markov Chain(MCMC) model - 
In the MCMC model, we first loop through the entire sentence and for each word, we get the probabilities for the corresponding part-of-speech and it is updated in a list. If no probability is available for a part-of-speech, we take the minimum probability and multiply it with a very low value( here 1e-15 ) to define its probability.
The probabilities are then normalised and their sum would be 1. These probability states are updated for every part-of-speech for every word in the prob list-of-lists

After this step, the main step of randomizing samples is implemented. An iteration number is chosen and an empty dictionary having all part-of-speech is initialized to zero. 
We then use the following function -

random.choices(all_pos,weights=prob[i],k=1)

where 

all_pos : All parts of speech

weights : Probabilities of the part-of-speech for each word which is derived from the prob list-of-lists 

k : Number of choices chosen

In the above function, we choose the part-of-speech based on their corresponding probabilities for the word. Upon implementing this, the part-of-speech chosen the maximum number of times after n iterations( here 4500) is iteratively updated in a list which is then returned as output.

##### Defining the log of joint probability P(S,W) - 

For Simple Model,

Log base 10 (emission probability of word and part-of-speech) + Log base 10 (Overall probability of part-of-speech) is taken for each word. 
For the test words not in list of train words, Log base 10 (random value) + Log base 10 (Overall probability of part-of-speech) is considered where the random value is made sure not to exceed 0.5.
Finally, all the values are summed up and returned as the log value of joint probability of simple model.

For Viterbi Model,

We first initialize our value to the Log base 10 (overall probability of the first part-of-speech).
Then, we add the values the same way as done in the simple model. In addition to that, we also add the Log base 10 (transition probability of part-of-speech to the next part-of-speech).
Finally, all the values are summed up and returned as the log value of joint probability of viterbi model.

For the MCMC Model,

We first initialize our value to the Log base 10 (overall probability of the first part-of-speech).
Then, we add the values the same way as done in the viterbi model. In addition to that, we also add the Log base 10 (transition probability of part-of-speech to the two consecutive part-of-speech).
Finally, all the values are summed up and returned as the log value of joint probability of mcmc model. 

### Description of the program:
The program first takes in the train dataset and defined the probabilities of emission and transition for the words and the different parts of speech. The code then computes the different defined probability models - Simple, Viterbi and MCMC models and gets computed as described above.
In addition to this, the program also returns the log of joint probability of P(S,W) for all the three probabilistic models.

### Problems faced and Design decisions:
##### Problems faced -
One of the main problems we faced was the implementation of the models and getting the values for the test words not defined in the train dataset. Initially, we randomly assigned a fixed value but since we were not getting good accuracy, a different approach was taken.
We randomized for all the probabilities we had to consider as described in the code to normalize our values and this made it more accurate. 

##### Design decisions - 
The designs for the Simple and Viterbi were good and did not face any problems but that was not the case for the MCMC model. 

Initially, we got a sample value and from this sample, a gen_sample function was defined which would take this sample and iteratively generate n samples based on their log probability for each word and the different parts of speech. After getting their log probability, the probabilities were cumulatively summed up and each value was compared with a generated random value.

If the cumulative value was greater than the random value, the sample part-of-speech with this new one and the process was repeated. The issues with this was the time taken and due to wrong implementation, the accuracy was not more than 5%.
We then implemented the above algorithm thus reaching ~91% for words and ~36% for sentences.


# Part 2: Ice-Tracking

## How I formulated my program:

In the case simple bayes net implementation I simply multiplied the prior with the likelihood to get the posterior.

I consider the prior to be the edge strength and to normalize to get the accurate probability I divide it by the pixel strength from Image array.

In the case Viterbi and Viterbi using human feedback the transition probability is considered with the inverse of the distance. As in if the previous pixels distance from the current pixel is 1/(abs(current_index – previous_index) + 1). 

Also to get a smoothening line a threshold of 3 pixels above and below the current pixel are considered.




## Brief description of how my program works:

In the case of simple bayes net for more obtaining more accuracy I computed the index of the 2 boundaries keeping the assumption that both the boundaries for a particular column has a difference of 10 pixels. 

After finding the bound of the first pixel of each boundary, I calculate the rest of the boundary pixels by keeping this as reference.


The code for the human feedback runs under the assumption as provided in the assignment question that is the row coordinate of the ice-bedrock boundary is 10 pixels greater than the air-ice boundary pixel for that column.

In the case of HMM Viterbi implementation, since the air-ice boundary has a darker line compared to the ice-bedrock boundary, the air-ice boundary is first predicted and lager keeping the air ice boundary as the index the ice-bedrock boundary is predicted.

Her in Viterbi, for the transition state I’m only considering the 3 pixels before and 3 pixels after the current pixel. This is basically done to get better smoothness of the line. And also, the transition probability decreases if the distance from the current pixel increases (The weight is considered to be inverse of distance)

In the case Viterbi using human feedback, considering the provided coordinates as index the boundaries after the point and the boundaries before the points are calculated. The thought process behind using this way is that it will take into the consideration the missing point and include that in the backtracked list to get a better boundary. This is clearly explained from the pictures below.



Below are the few outputs of the problem.

## Fig 23:

![Fig 23: Simple](Fig23_simple.png)

This is Simple Bayes Net implementation and we could see that the yellow boundary lines are very discrete and they are not really smooth along the boundary line.

![Fig 23: Viterbi](Fig23_viterbi.png)

Here using a Viterbi algorithm it provides better result than the simple Bayes net but from the round marker you can see that some minute boundaries are not predicted properly.

Now using human feedback-coordinates :

For Air-Ice boundary providing human feedback coordinates of (38,118) and Ice-Bedrock boundary providing human feedback coordinates of (81,118)


![Fig 23: Human Feedback](Fig23_human_feedback.png)

Here it comparatively performs better than just the Viterbi as the human feedback point considers the boundaries that were missed.

## Fig 30

![Fig 30: Simple](Fig30_simple.png)

This is a simple Bayes net implementatio for Fig30.

![Fig 30: Viterbi](Fig30_viterbi.png)

This is viterbi HMM  implementation for Fig 30 consisting a better smoothened line.

Now using human feedback-coordinates :

For Air-Ice boundary providing human feedback coordinates of (23,118) and Ice-Bedrock boundary providing human feedback coordinates of (59,118)


![Fig 30: Human Feedback](Fig30_human_feedback.png)

The difficulties faced while implementing the code were that:

The air-ice pixel strength were so strong that it was interfering with the probabilities of the second ice-bedrock pixels and hence I had to do some more implementations to tackle such problem for the ice-bedrock.

# Part 3: Reading text

#### Assumptions: 
That these images have English words and sentences, each letter fits in a box that’s 16 pixels wide and 25 pixels tall. We’ll also assume that our documents only have the 26 uppercase latin characters, the 26 lowercase characters, the 10 digits, spaces, and 7 punctuation symbols, (),.-!?’".

The following two approaches were used for reading text from images:
1.	Naive Bayes method : For the emission probability, we used a simple naive Bayes classifier
2.	Viterbi algorithm

#### Firstly, we train the data, and store the emission, transition probabilities in a dictionary.

The dictionaries store:
1.	Probability of word given speech.
O1, ..., On and n hidden variables, l1..., ln, which are
the letters we want to recognize. We’re thus interested in P (l1, ..., ln|O1, ..., On).
2.	Transition probabilities 
The above probabilities are stored to use further for the algos.

#### How program works:
We have used the list of dictionaries to represent the Viterbi table emisson_pixel{}. The key to the dictionary component of letter we're working on right now. The Viterbi list's index denotes the letter for which we intend to locate the letter of test image. We calculate the maximum value of all parts of talks for a particular letter, and then assign that value to a cell in the Viterbi table (for given letter). The path that this algorithm takes is saved in another dictionary, and fresh parts of speech are added to the Viterbi path at each step. Finally, we compute the maximum and return the path for this maximum segment of speech, which is the path taken by our Viterbi method.
#### Challenges faced:

###### We comapring pixel values for emission probabilities between train image and test image. Due to high noise in images the white space was overpowering and hence to resolve this weighted sum was taken. Giving "*" more priority than " " (white space)
#### Design decisions: 

###### Data structure Dictionary – we used dictionaries because of the easy access to their values and constant time for fetching

#### Results of this evaluation on bc.train file and test image test_images/test-5-0.png were:

1. Simple: Opinion"of!the'Court
2. HMM: Opinion oflthe'Court
   


