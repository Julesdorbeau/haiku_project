#  Projet de Machine Learning : Génération d'Haïkus Multilingues

Ce projet vise à développer un modèle de machine learning capable de générer des haïkus en plusieurs langues. En collectant des données d'haïkus provenant de diverses sources en ligne, nous entraînons un modèle LSTM (Long Short-Term Memory) pour générer des haïkus à partir d'une amorce donnée.

---

## Objectifs :
- Collecter des haïkus dans différentes langues à partir de sites web.
- Nettoyer et structurer les données pour pouvoir les utiliser avec les modèles sélectionnés.
- Entraîner un modèle LSTM capable de générer des haïkus à partir d’un début de ligne ou d'une ligne complète.

---

## Prochaines Évolutions :

### Optimisation de l'entraînement du modèle
- [ ] Retravailler le pipeline d'entraînement pour permettre le chargement progressif des données à chaque epoch.  
  - **Problème actuel** : Le modèle utilise toute la mémoire disponible en chargeant l'intégralité du dataset.
  - **Solution attendue** : Implémenter un système de chargement par batch ou utiliser des data generators avec TensorFlow.

### Migration et alternative avec PyTorch
- [ ] Développer une version de l’entraînement avec PyTorch.  
  - **Motivation** : Découvrir les avantages de PyTorch et comparer les performances avec TensorFlow.

### Augmentation de la taille du dataset
- [ ] Collecter davantage de données pour enrichir le dataset.  
  - **Objectif** : Évaluer l’impact de la taille du dataset sur les performances du modèle.
  - **Actions associées** : Automatiser et étendre les processus de web scraping.

### Exploration de nouveaux modèles
- [ ] Tester d’autres architectures de machine learning.  
  - **Exemples à explorer** : Transformers, GRU, ou modèles pré-entraînés spécialisés dans le traitement du texte.
  - **But** : Identifier des modèles plus modernes et performants que le LSTM.

### Développement d'une interface pour le web scraping
- [ ] Créer une interface graphique pour simplifier le web scraping avec BeautifulSoup.  
  - **Fonctionnalités attendues** :  
    - Visualisation en direct des résultats des requêtes.  
    - Intégration de plusieurs librairies de web scraping pour explorer d'autres outils.
  - **Motivation** : Gagner en efficacité et améliorer l’expérience utilisateur dans la collecte de données.

---
     
# Machine Learning Project: Multilingual Haiku Generation

This project aims to develop a machine learning model capable of generating haikus in multiple languages. By collecting haiku data from various online sources, we train an LSTM (Long Short-Term Memory) model to generate haikus based on a given prompt.

---

## Objectives:
- Collect haikus in different languages from websites.
- Clean and structure the data to make it usable with the selected models.
- Train an LSTM model capable of generating haikus from a starting line or a complete prompt.

---

## Future Developments:

### Optimizing the Training Pipeline
- [ ] Redesign the training pipeline to allow progressive loading of data for each epoch.  
  - **Current Issue**: The model uses all available memory by loading the entire dataset at once.  
  - **Proposed Solution**: Implement a batch loading system or use data generators with TensorFlow.

### Migration and Alternative with PyTorch
- [ ] Develop a training version using PyTorch.  
  - **Motivation**: Explore the benefits of PyTorch and compare its performance with TensorFlow.

### Expanding the Dataset
- [ ] Collect more data to enrich the dataset.  
  - **Objective**: Assess the impact of dataset size on model performance.  
  - **Associated Actions**: Automate and expand web scraping processes.

### Exploring New Models
- [ ] Test other machine learning architectures.  
  - **Examples to Explore**: Transformers, GRU, or pre-trained models specialized in text processing.  
  - **Goal**: Identify more modern and efficient models than the LSTM.

### Developing a Web Scraping Interface
- [ ] Create a graphical interface to simplify web scraping with BeautifulSoup.  
  - **Expected Features**:  
    - Real-time visualization of query results.  
    - Integration of multiple web scraping libraries to explore other tools.  
  - **Motivation**: Improve efficiency and user experience in data collection.

