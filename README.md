# Diffusion-LM for Piano Music Generation 

**Collaborators:** [Janavi Kasera](https://github.com/janavikasera) and [Ruiqi Liu](https://github.com/RRQLiu).

**Disclaimer**: This is a course project of Boston University's CAS CS 523: Deep Learning.

This repository contains the implementation of our innovative project for generating piano music using Diffusion Language Models (Diffusion-LM). Our method was inspired by the potential of these models to generate complex, structured data. Specifically, we adapted the models to generate discrete sequences of MIDI music data. This project explores both BERT and Electra-BERT as base networks for the diffusion model.

## Table of Contents

- [Introduction](#Introduction)
- [Datasets](#Datasets)
- [Methodology](#Methodology)
- [Results](#Results)
- [Sample Output](#Sample-Output)

## Introduction

The aim of our project was to explore the potential of Diffusion Language Models in generating discrete piano music. We fed MIDI files into the system, which were then tokenized into a format suitable for the diffusion model. The model generates music by optimizing a language model, demonstrating a novel application of these models beyond their traditional use in natural language processing. In this project, we experimented with two versions of the diffusion model, one with BERT and one with Electra-BERT as the base network.

## Datasets

Our project used the Lakh Large MIDI dataset, a collection of over 10,000 piano MIDI files. The dataset was pre-processed and tokenized to generate sequences of musical notation in a text format, which the diffusion model could then learn to generate. If you want to use this dataset, you can download it [here](https://colinraffel.com/projects/lmd/#get).

## Methodology

Our project employs a novel approach of training a Diffusion-LM model on MIDI files using BERT transformer model and Electra-BERT to generate discrete music. Here are the detailed steps:

1. **Data Preparation**: Our dataset is composed of MIDI files from the Lakh MIDI dataset. The MIDI files are transposed into a unified key to reduce the complexity of the model's training.

2. **Preprocessing**: The MIDI files are then converted into text using the python MIDI library. This library translates the MIDI files into a sequence of musical events such as note-on, note-off, time-shifts etc. Each of these events are then encoded into a unique token, and the sequences of these tokens form the input data for our model.

3. **Model Training**: We train a Diffusion Language Model (Diffusion-LM) on the tokenized MIDI data. The Diffusion-LM model is built upon a BERT transformer model, where the transformer is used to parameterize a Gaussian diffusion process. The transformer takes the raw MIDI tokens as input, and produces as output a distribution over next tokens, from which a token is sampled and fed into the next step of the transformer. The model is trained with forward and reverse steps to optimize the likelihood of the generated music.

4. **Evaluation**: The quality of the music generated by the model is evaluated using bit-per-word (bpw) metric. The bpw measures the frequency of the generated sentences, assuming that a sentence with less-frequent words is more difficult to generate.

$$\begin{equation}
    \begin{split}
        bpw(token) = \frac{1}{T}\sum\limits_{t=1}^{T}H(P_t, \hat{P}_t) 
        & = - \frac{1}{T} \sum\limits_{t=1}^{T}
        \sum\limits_{c=1}^{n} P_t(c)\log_2\hat{P_t}(c)\\
        & = - \frac{1}{T} \sum\limits_{t=1}^{T}\log_2\hat{P}_t(x_t)
    \end{split}
\end{equation}

$$

5. **MIDI and Waveform Visualization**: The generated MIDI files are visualized using MIDI visualization tools and waveforms are used to show the timing and duration of notes in the music.

## Results

Our results are predominantly derived from training a Diffusion Language Model (Diffusion-LM) using BERT and Electra-BERT transformers.

The most optimal results were achieved with BERT transformer after 800 iterations. The model yielded coherent music generation with a low bit-per-word (bpw) score of 0.00003, indicating higher frequency of generated sentences.

The generated MIDI files and corresponding waveforms are available in the repository for visualization. We observed some gaps between the notes in the generated music, indicating areas for further optimization.

For a more detailed evaluation and visualizations, kindly refer to the 'Results' folder in this repository.

However, it's important to note that these results are dependent on the parameters and data used for training. Results may vary with different datasets or parameter settings.

| Model                    | Iterations | Steps | bits-per-word |
|--------------------------|------------|-------|---------------|
| Diffusion-LM using BERT  | 800        | 2000  | 0.00003       |
| Diffusion-LM using BERT  | 1000       | 2000  | 0.00004       |
| Diffusion-LM using BERT  | 2000       | 2000  | 0.00007       |
| Diffusion-LM using Electra| 1000       | 2000  | 0.00020       |
| Diffusion-LM using Electra| 2000       | 2000  | 0.00030       |

## Sample-Output

<audio src="sample_output/output_1.wav" controls title="Title"></audio>

<audio src="sample_output/output_2.wav" controls title="Title"></audio>

<audio src="sample_output/output_3.wav" controls title="Title"></audio>

<audio src="sample_output/output_4.wav" controls title="Title"></audio>



