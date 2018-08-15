## Social Trust Model

Matlab files for the proposed social trust model for Epinions dataset. 

## A. Installation

No installation is required 

## B. Code structure

1. Centrality.m: capture user centrality based on various centrality measures: degree, eigen, Katz and PageRank centrality.

2. Fact.m: apply matrix factorization method to map both users and items to a joint latent factor space so the user-item interactions are modeled as a inner products in such space. 

3. Similarity.m: capture two types of similarity between users. Connection similarity and rating similarity. Rating similarity also consists of PCC and VSS similarity. 

## C. Inputs

input_s.mat: this file consists of two matrices: 1) user-item rating matrix and 2) user-user trust matrix.

## D. Publications

Anahita Davoudi, and Mainak Chatterjee, Social Trust Model for Rating Prediction in Recommender Systems: Effects of Similarity, Centrality, and Social Ties, Journal of Online Social Networks and Media (OSNEM), Elsevier, July 2018.