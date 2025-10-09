"""
NLP Models - Modelos de processamento de linguagem natural
Análise de sentimento, classificação de texto, extração de entidades
"""

import torch
import torch.nn as nn
from transformers import (
    AutoTokenizer, AutoModel, 
    BertForSequenceClassification, BertTokenizer,
    RobertaForSequenceClassification, RobertaTokenizer
)
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re
from collections import Counter
import json

logger = logging.getLogger(__name__)

@dataclass
class SentimentResult:
    """Resultado de análise de sentimento"""
    sentiment: str  # positive, negative, neutral
    confidence: float
    scores: Dict[str, float]

@dataclass
class TextClassificationResult:
    """Resultado de classificação de texto"""
    category: str
    confidence: float
    all_scores: Dict[str, float]

@dataclass
class EntityRecognitionResult:
    """Resultado de reconhecimento de entidades"""
    text: str
    entities: List[Dict[str, Any]]

@dataclass
class TextSummary:
    """Resultado de sumarização de texto"""
    summary: str
    original_length: int
    summary_length: int
    compression_ratio: float

class SentimentAnalysisModel(nn.Module):
    """Modelo para análise de sentimento"""
    
    def __init__(self, num_labels: int = 3, hidden_size: int = 768):
        super().__init__()
        self.bert = BertForSequenceClassification.from_pretrained(
            'neuralmind/bert-base-portuguese-cased',
            num_labels=num_labels
        )
        self.num_labels = num_labels
        
    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )
        return outputs

class TextClassificationModel(nn.Module):
    """Modelo para classificação de texto"""
    
    def __init__(self, num_categories: int = 10, hidden_size: int = 768):
        super().__init__()
        self.roberta = RobertaForSequenceClassification.from_pretrained(
            'neuralmind/roberta-base-portuguese-cased',
            num_labels=num_categories
        )
        self.num_categories = num_categories
        
    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.roberta(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )
        return outputs

class EntityRecognitionModel(nn.Module):
    """Modelo para reconhecimento de entidades nomeadas"""
    
    def __init__(self, num_entities: int = 9, hidden_size: int = 768):
        super().__init__()
        self.bert = AutoModel.from_pretrained('neuralmind/bert-base-portuguese-cased')
        self.classifier = nn.Linear(hidden_size, num_entities)
        self.num_entities = num_entities
        
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = outputs.last_hidden_state
        logits = self.classifier(sequence_output)
        return logits

class NLPService:
    """Serviço de processamento de linguagem natural"""
    
    def __init__(self, device: str = "cpu"):
        self.device = torch.device(device)
        
        # Inicializar modelos
        self.sentiment_model = SentimentAnalysisModel()
        self.classification_model = TextClassificationModel()
        self.entity_model = EntityRecognitionModel()
        
        # Inicializar tokenizers
        self.sentiment_tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
        self.classification_tokenizer = RobertaTokenizer.from_pretrained('neuralmind/roberta-base-portuguese-cased')
        self.entity_tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
        
        # Mover modelos para device
        self.sentiment_model.to(self.device)
        self.classification_model.to(self.device)
        self.entity_model.to(self.device)
        
        # Configurar modo de avaliação
        self.sentiment_model.eval()
        self.classification_model.eval()
        self.entity_model.eval()
        
        # Categorias de classificação
        self.categories = [
            'feedback', 'bug_report', 'feature_request', 'complaint',
            'praise', 'question', 'suggestion', 'complaint_resolution',
            'product_inquiry', 'service_request'
        ]
        
        # Entidades nomeadas
        self.entity_types = [
            'PERSON', 'ORGANIZATION', 'LOCATION', 'MONEY', 'PERCENT',
            'DATE', 'TIME', 'PRODUCT', 'OTHER'
        ]
    
    def analyze_sentiment(self, text: str) -> SentimentResult:
        """Analisar sentimento do texto"""
        try:
            # Tokenizar texto
            inputs = self.sentiment_tokenizer(
                text,
                return_tensors='pt',
                truncation=True,
                padding=True,
                max_length=512
            ).to(self.device)
            
            # Fazer predição
            with torch.no_grad():
                outputs = self.sentiment_model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1)
            
            # Processar resultados
            sentiment_labels = ['negative', 'neutral', 'positive']
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = float(probabilities[0, predicted_class])
            
            # Criar scores para todas as classes
            scores = {
                label: float(probabilities[0, i]) 
                for i, label in enumerate(sentiment_labels)
            }
            
            result = SentimentResult(
                sentiment=sentiment_labels[predicted_class],
                confidence=confidence,
                scores=scores
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na análise de sentimento: {e}")
            return SentimentResult(
                sentiment='neutral',
                confidence=0.0,
                scores={'negative': 0.33, 'neutral': 0.34, 'positive': 0.33}
            )
    
    def classify_text(self, text: str, categories: List[str] = None) -> TextClassificationResult:
        """Classificar texto em categorias"""
        try:
            # Usar categorias fornecidas ou padrão
            if categories is None:
                categories = self.categories
            
            # Tokenizar texto
            inputs = self.classification_tokenizer(
                text,
                return_tensors='pt',
                truncation=True,
                padding=True,
                max_length=512
            ).to(self.device)
            
            # Fazer predição
            with torch.no_grad():
                outputs = self.classification_model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1)
            
            # Processar resultados
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = float(probabilities[0, predicted_class])
            
            # Criar scores para todas as categorias
            all_scores = {
                categories[i]: float(probabilities[0, i]) 
                for i in range(min(len(categories), probabilities.size(1)))
            }
            
            result = TextClassificationResult(
                category=categories[predicted_class],
                confidence=confidence,
                all_scores=all_scores
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na classificação de texto: {e}")
            return TextClassificationResult(
                category='feedback',
                confidence=0.0,
                all_scores={cat: 0.1 for cat in categories}
            )
    
    def recognize_entities(self, text: str) -> EntityRecognitionResult:
        """Reconhecer entidades nomeadas no texto"""
        try:
            # Tokenizar texto
            inputs = self.entity_tokenizer(
                text,
                return_tensors='pt',
                truncation=True,
                padding=True,
                max_length=512
            ).to(self.device)
            
            # Fazer predição
            with torch.no_grad():
                logits = self.entity_model(**inputs)
                predictions = torch.argmax(logits, dim=2)
            
            # Processar resultados
            tokens = self.entity_tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
            entities = []
            current_entity = None
            
            for i, (token, pred) in enumerate(zip(tokens, predictions[0])):
                if token.startswith('##'):
                    continue
                
                entity_type = self.entity_types[pred.item()]
                
                if entity_type != 'OTHER':
                    if current_entity is None or current_entity['type'] != entity_type:
                        if current_entity:
                            entities.append(current_entity)
                        current_entity = {
                            'text': token,
                            'type': entity_type,
                            'start': i,
                            'end': i
                        }
                    else:
                        current_entity['text'] += ' ' + token
                        current_entity['end'] = i
                else:
                    if current_entity:
                        entities.append(current_entity)
                        current_entity = None
            
            if current_entity:
                entities.append(current_entity)
            
            result = EntityRecognitionResult(
                text=text,
                entities=entities
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Erro no reconhecimento de entidades: {e}")
            return EntityRecognitionResult(
                text=text,
                entities=[]
            )
    
    def summarize_text(self, text: str, max_length: int = 100) -> TextSummary:
        """Sumarizar texto"""
        try:
            # Implementação simples de sumarização
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if len(sentences) <= 1:
                return TextSummary(
                    summary=text,
                    original_length=len(text),
                    summary_length=len(text),
                    compression_ratio=1.0
                )
            
            # Selecionar sentenças mais importantes (simulação)
            important_sentences = sentences[:max(1, len(sentences) // 2)]
            summary = '. '.join(important_sentences) + '.'
            
            result = TextSummary(
                summary=summary,
                original_length=len(text),
                summary_length=len(summary),
                compression_ratio=len(summary) / len(text)
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na sumarização: {e}")
            return TextSummary(
                summary=text[:max_length] + '...' if len(text) > max_length else text,
                original_length=len(text),
                summary_length=min(len(text), max_length),
                compression_ratio=min(len(text), max_length) / len(text)
            )
    
    def extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """Extrair palavras-chave do texto"""
        try:
            # Limpar texto
            text = re.sub(r'[^\w\s]', '', text.lower())
            words = text.split()
            
            # Remover stopwords (lista básica em português)
            stopwords = {
                'a', 'o', 'e', 'de', 'do', 'da', 'em', 'na', 'no', 'para', 'por',
                'com', 'sem', 'sobre', 'entre', 'até', 'desde', 'durante', 'após',
                'que', 'quem', 'onde', 'quando', 'como', 'porque', 'se', 'mas',
                'então', 'também', 'muito', 'mais', 'menos', 'bem', 'mal', 'sempre',
                'nunca', 'já', 'ainda', 'só', 'apenas', 'tanto', 'quanto', 'cada',
                'todo', 'toda', 'todos', 'todas', 'algum', 'alguma', 'alguns',
                'algumas', 'nenhum', 'nenhuma', 'nenhuns', 'nenhumas'
            }
            
            # Filtrar palavras
            filtered_words = [word for word in words if word not in stopwords and len(word) > 2]
            
            # Contar frequência
            word_freq = Counter(filtered_words)
            
            # Retornar palavras mais frequentes
            keywords = [word for word, freq in word_freq.most_common(num_keywords)]
            
            return keywords
            
        except Exception as e:
            logger.error(f"Erro na extração de palavras-chave: {e}")
            return []
    
    def analyze_customer_feedback(self, feedback: str) -> Dict[str, Any]:
        """Analisar feedback do cliente"""
        try:
            # Análise de sentimento
            sentiment = self.analyze_sentiment(feedback)
            
            # Classificação do texto
            classification = self.classify_text(feedback)
            
            # Reconhecimento de entidades
            entities = self.recognize_entities(feedback)
            
            # Extração de palavras-chave
            keywords = self.extract_keywords(feedback)
            
            # Sumarização
            summary = self.summarize_text(feedback)
            
            analysis = {
                'sentiment': {
                    'label': sentiment.sentiment,
                    'confidence': sentiment.confidence,
                    'scores': sentiment.scores
                },
                'classification': {
                    'category': classification.category,
                    'confidence': classification.confidence,
                    'all_scores': classification.all_scores
                },
                'entities': entities.entities,
                'keywords': keywords,
                'summary': {
                    'text': summary.summary,
                    'compression_ratio': summary.compression_ratio
                },
                'metadata': {
                    'original_length': len(feedback),
                    'summary_length': summary.summary_length,
                    'num_entities': len(entities.entities),
                    'num_keywords': len(keywords)
                }
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro na análise de feedback: {e}")
            return {
                'error': str(e),
                'sentiment': {'label': 'neutral', 'confidence': 0.0},
                'classification': {'category': 'feedback', 'confidence': 0.0},
                'entities': [],
                'keywords': [],
                'summary': {'text': feedback[:100] + '...', 'compression_ratio': 0.5}
            }
