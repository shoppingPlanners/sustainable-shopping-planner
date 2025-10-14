"""
Rating Calculator Agent - Analyzes data and assigns sustainability scores.
"""
import asyncio
import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from textblob import TextBlob
import spacy

from agents.shared.communication.mcp_protocol import MCPAgent, AgentRole
from shared.database.base import get_db
from shared.models.brand import Brand, Product, SustainabilityMetric
from shared.models.rating import SustainabilityRating, RatingHistory
from config.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class RatingComponents:
    """Components that contribute to sustainability rating."""
    environmental_score: float
    social_score: float
    economic_score: float
    carbon_footprint_score: float
    water_usage_score: float
    waste_reduction_score: float
    ethical_sourcing_score: float
    worker_rights_score: float
    community_impact_score: float
    price_fairness_score: float
    durability_score: float
    confidence_score: float
    data_completeness: float


class SustainabilityNLPAnalyzer:
    """NLP analyzer for sustainability content."""
    
    def __init__(self):
        self.llm = OpenAI(
            api_key=settings.openai_api_key,
            temperature=0.1,
            max_tokens=500
        )
        
        # Load spaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. NER features will be limited.")
            self.nlp = None
        
        # Sustainability sentiment keywords
        self.positive_keywords = [
            'reduce', 'renewable', 'sustainable', 'eco-friendly', 'carbon neutral',
            'zero waste', 'recycled', 'biodegradable', 'fair trade', 'ethical',
            'clean energy', 'green', 'responsible', 'conservation', 'efficiency'
        ]
        
        self.negative_keywords = [
            'pollution', 'waste', 'harmful', 'toxic', 'unsustainable',
            'deforestation', 'exploitation', 'child labor', 'unfair'
        ]
    
    async def analyze_commitment_quality(self, commitments: List[str]) -> Dict[str, float]:
        """Analyze the quality and specificity of sustainability commitments."""
        
        if not commitments:
            return {'quality_score': 0.0, 'specificity_score': 0.0, 'sentiment_score': 0.5}
        
        scores = []
        sentiment_scores = []
        specificity_scores = []
        
        for commitment in commitments:
            # Analyze sentiment
            sentiment = TextBlob(commitment).sentiment
            sentiment_scores.append(max(0, sentiment.polarity))  # Convert to 0-1 range
            
            # Analyze specificity (presence of numbers, dates, targets)
            specificity = self._calculate_specificity(commitment)
            specificity_scores.append(specificity)
            
            # Overall quality using LLM
            quality = await self._analyze_with_llm(commitment)
            scores.append(quality)
        
        return {
            'quality_score': np.mean(scores) if scores else 0.0,
            'specificity_score': np.mean(specificity_scores),
            'sentiment_score': np.mean(sentiment_scores)
        }
    
    def _calculate_specificity(self, text: str) -> float:
        """Calculate specificity score based on concrete details."""
        import re
        
        score = 0.0
        
        # Check for numbers and percentages
        if re.search(r'\d+%', text):
            score += 0.3
        if re.search(r'\d{4}', text):  # Years
            score += 0.2
        if re.search(r'\d+', text):  # Any numbers
            score += 0.1
        
        # Check for specific action words
        action_words = ['reduce', 'eliminate', 'achieve', 'implement', 'target', 'commit']
        for word in action_words:
            if word in text.lower():
                score += 0.1
                break
        
        # Check for timeframes
        timeframe_words = ['by', 'until', 'within', 'before', 'after']
        for word in timeframe_words:
            if word in text.lower():
                score += 0.2
                break
        
        # Check for quantifiable outcomes
        outcome_words = ['carbon neutral', 'net zero', 'renewable energy', 'waste reduction']
        for phrase in outcome_words:
            if phrase in text.lower():
                score += 0.1
        
        return min(score, 1.0)
    
    async def _analyze_with_llm(self, commitment: str) -> float:
        """Use LLM to analyze commitment quality."""
        
        prompt = PromptTemplate(
            input_variables=["commitment"],
            template="""
            Analyze this sustainability commitment and rate its quality on a scale of 0.0 to 1.0:
            
            Commitment: "{commitment}"
            
            Consider:
            - Specificity (concrete goals vs vague statements)
            - Measurability (quantifiable targets)
            - Timeframe (clear deadlines)
            - Credibility (realistic and achievable)
            - Impact potential (meaningful environmental/social benefit)
            
            Return only a number between 0.0 and 1.0:
            """
        )
        
        try:
            formatted_prompt = prompt.format(commitment=commitment)
            response = await asyncio.get_event_loop().run_in_executor(
                None, self.llm, formatted_prompt
            )
            
            # Extract numeric score
            import re
            score_match = re.search(r'(\d*\.?\d+)', response.strip())
            if score_match:
                score = float(score_match.group(1))
                return min(max(score, 0.0), 1.0)  # Clamp to 0-1 range
            
        except Exception as e:
            logger.error(f"LLM analysis error: {e}")
        
        return 0.5  # Default neutral score
    
    def extract_metrics_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract quantitative metrics from text using NER and pattern matching."""
        
        metrics = []
        
        if self.nlp:
            doc = self.nlp(text)
            
            # Extract quantities and percentages
            for ent in doc.ents:
                if ent.label_ in ['PERCENT', 'QUANTITY', 'CARDINAL']:
                    context = text[max(0, ent.start_char-50):ent.end_char+50]
                    
                    # Determine metric type from context
                    metric_type = self._classify_metric_type(context.lower())
                    if metric_type:
                        metrics.append({
                            'type': metric_type,
                            'value': ent.text,
                            'context': context,
                            'confidence': 0.8
                        })
        
        # Pattern-based extraction as fallback
        import re
        patterns = [
            (r'(\d+)%.*carbon.*reduc', 'carbon_reduction'),
            (r'(\d+)%.*renewable.*energy', 'renewable_energy'),
            (r'(\d+)%.*waste.*reduc', 'waste_reduction'),
            (r'(\d+)%.*water.*sav', 'water_saving'),
            (r'net zero.*(\d{4})', 'net_zero_target'),
            (r'carbon neutral.*(\d{4})', 'carbon_neutral_target')
        ]
        
        for pattern, metric_type in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                metrics.append({
                    'type': metric_type,
                    'value': match.group(1),
                    'context': text[max(0, match.start()-30):match.end()+30],
                    'confidence': 0.6
                })
        
        return metrics
    
    def _classify_metric_type(self, context: str) -> Optional[str]:
        """Classify the type of sustainability metric from context."""
        
        classifications = {
            'carbon': ['carbon_footprint', 'carbon_reduction', 'carbon_neutral'],
            'energy': ['renewable_energy', 'energy_efficiency'],
            'water': ['water_usage', 'water_conservation'],
            'waste': ['waste_reduction', 'zero_waste'],
            'emission': ['emission_reduction', 'greenhouse_gas'],
            'recycl': ['recycling_rate', 'circular_economy']
        }
        
        for key, types in classifications.items():
            if key in context:
                # Return the most specific type based on additional context
                for metric_type in types:
                    type_words = metric_type.split('_')
                    if all(word in context for word in type_words):
                        return metric_type
                return types[0]  # Return first as default
        
        return None


class SustainabilityScorer:
    """Calculate sustainability scores based on multiple factors."""
    
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.ml_model = None
        self.weights = {
            'environmental': 0.4,
            'social': 0.35,
            'economic': 0.25
        }
        
        # Sub-component weights
        self.environmental_weights = {
            'carbon_footprint': 0.3,
            'water_usage': 0.2,
            'waste_reduction': 0.25,
            'renewable_energy': 0.25
        }
        
        self.social_weights = {
            'ethical_sourcing': 0.3,
            'worker_rights': 0.4,
            'community_impact': 0.3
        }
        
        self.economic_weights = {
            'price_fairness': 0.6,
            'durability': 0.4
        }
    
    async def calculate_comprehensive_score(self, 
                                          brand: Brand, 
                                          product: Optional[Product] = None,
                                          nlp_analysis: Optional[Dict] = None) -> RatingComponents:
        """Calculate comprehensive sustainability score."""
        
        # Environmental score
        env_score = await self._calculate_environmental_score(brand, product, nlp_analysis)
        
        # Social score  
        social_score = await self._calculate_social_score(brand, product, nlp_analysis)
        
        # Economic score
        economic_score = await self._calculate_economic_score(brand, product)
        
        # Individual component scores
        carbon_score = await self._calculate_carbon_footprint_score(brand, product)
        water_score = await self._calculate_water_usage_score(brand, product)
        waste_score = await self._calculate_waste_reduction_score(brand, product)
        ethical_score = await self._calculate_ethical_sourcing_score(brand, product)
        worker_score = await self._calculate_worker_rights_score(brand, product)
        community_score = await self._calculate_community_impact_score(brand, product)
        price_score = await self._calculate_price_fairness_score(brand, product)
        durability_score = await self._calculate_durability_score(brand, product)
        
        # Calculate confidence and data completeness
        confidence = self._calculate_confidence_score(brand, product, nlp_analysis)
        completeness = self._calculate_data_completeness(brand, product)
        
        return RatingComponents(
            environmental_score=env_score,
            social_score=social_score,
            economic_score=economic_score,
            carbon_footprint_score=carbon_score,
            water_usage_score=water_score,
            waste_reduction_score=waste_score,
            ethical_sourcing_score=ethical_score,
            worker_rights_score=worker_score,
            community_impact_score=community_score,
            price_fairness_score=price_score,
            durability_score=durability_score,
            confidence_score=confidence,
            data_completeness=completeness
        )
    
    async def _calculate_environmental_score(self, 
                                           brand: Brand, 
                                           product: Optional[Product],
                                           nlp_analysis: Optional[Dict]) -> float:
        """Calculate environmental sustainability score."""
        
        scores = []
        
        # Carbon footprint component
        carbon_score = await self._calculate_carbon_footprint_score(brand, product)
        scores.append(('carbon_footprint', carbon_score, self.environmental_weights['carbon_footprint']))
        
        # Water usage component
        water_score = await self._calculate_water_usage_score(brand, product)
        scores.append(('water_usage', water_score, self.environmental_weights['water_usage']))
        
        # Waste reduction component
        waste_score = await self._calculate_waste_reduction_score(brand, product)
        scores.append(('waste_reduction', waste_score, self.environmental_weights['waste_reduction']))
        
        # Renewable energy component (estimated from commitments)
        renewable_score = self._estimate_renewable_energy_score(brand, nlp_analysis)
        scores.append(('renewable_energy', renewable_score, self.environmental_weights['renewable_energy']))
        
        # Calculate weighted average
        total_weight = sum(weight for _, _, weight in scores)
        if total_weight > 0:
            weighted_score = sum(score * weight for _, score, weight in scores) / total_weight
            return min(max(weighted_score * 100, 0), 100)  # Scale to 0-100
        
        return 50.0  # Default neutral score
    
    async def _calculate_social_score(self, 
                                    brand: Brand, 
                                    product: Optional[Product],
                                    nlp_analysis: Optional[Dict]) -> float:
        """Calculate social sustainability score."""
        
        scores = []
        
        # Ethical sourcing
        ethical_score = await self._calculate_ethical_sourcing_score(brand, product)
        scores.append(('ethical_sourcing', ethical_score, self.social_weights['ethical_sourcing']))
        
        # Worker rights
        worker_score = await self._calculate_worker_rights_score(brand, product)
        scores.append(('worker_rights', worker_score, self.social_weights['worker_rights']))
        
        # Community impact
        community_score = await self._calculate_community_impact_score(brand, product)
        scores.append(('community_impact', community_score, self.social_weights['community_impact']))
        
        # Calculate weighted average
        total_weight = sum(weight for _, _, weight in scores)
        if total_weight > 0:
            weighted_score = sum(score * weight for _, score, weight in scores) / total_weight
            return min(max(weighted_score * 100, 0), 100)
        
        return 50.0
    
    async def _calculate_economic_score(self, brand: Brand, product: Optional[Product]) -> float:
        """Calculate economic sustainability score."""
        
        scores = []
        
        # Price fairness
        price_score = await self._calculate_price_fairness_score(brand, product)
        scores.append(('price_fairness', price_score, self.economic_weights['price_fairness']))
        
        # Durability/longevity
        durability_score = await self._calculate_durability_score(brand, product)
        scores.append(('durability', durability_score, self.economic_weights['durability']))
        
        # Calculate weighted average
        total_weight = sum(weight for _, _, weight in scores)
        if total_weight > 0:
            weighted_score = sum(score * weight for _, score, weight in scores) / total_weight
            return min(max(weighted_score * 100, 0), 100)
        
        return 50.0
    
    async def _calculate_carbon_footprint_score(self, brand: Brand, product: Optional[Product]) -> float:
        """Calculate carbon footprint score."""
        
        score = 50.0  # Default neutral
        
        # Check for carbon-related metrics
        if brand.sustainability_metrics:
            for metric in brand.sustainability_metrics:
                if 'carbon' in metric.metric_type.lower():
                    # Higher values are worse for carbon footprint, so invert
                    normalized_value = min(metric.value / 100, 1.0)  # Assume 100 is max
                    score = (1 - normalized_value) * 100
                    break
        
        # Check certifications
        if brand.certifications:
            carbon_certs = ['Carbon Trust', 'Climate Neutral', 'Carbon Neutral']
            for cert in brand.certifications:
                if any(c.lower() in cert.lower() for c in carbon_certs):
                    score = max(score, 80.0)  # Boost score for certifications
                    break
        
        # Check commitments
        if brand.sustainability_commitments:
            commitments_text = str(brand.sustainability_commitments).lower()
            if any(term in commitments_text for term in ['carbon neutral', 'net zero', 'carbon negative']):
                score = max(score, 75.0)
        
        return score
    
    async def _calculate_water_usage_score(self, brand: Brand, product: Optional[Product]) -> float:
        """Calculate water usage efficiency score."""
        
        score = 50.0  # Default neutral
        
        # Check for water-related metrics
        if brand.sustainability_metrics:
            for metric in brand.sustainability_metrics:
                if 'water' in metric.metric_type.lower():
                    # Assume lower water usage is better
                    if 'reduction' in metric.metric_type.lower():
                        score = min(metric.value, 100)  # Direct score for reduction percentage
                    else:
                        # Invert if it's usage amount
                        normalized_value = min(metric.value / 1000, 1.0)  # Assume 1000 is max
                        score = (1 - normalized_value) * 100
                    break
        
        # Check commitments
        if brand.sustainability_commitments:
            commitments_text = str(brand.sustainability_commitments).lower()
            if any(term in commitments_text for term in ['water conservation', 'water efficiency', 'water saving']):
                score = max(score, 70.0)
        
        return score
    
    async def _calculate_waste_reduction_score(self, brand: Brand, product: Optional[Product]) -> float:
        """Calculate waste reduction score."""
        
        score = 50.0
        
        # Check for waste-related metrics
        if brand.sustainability_metrics:
            for metric in brand.sustainability_metrics:
                if 'waste' in metric.metric_type.lower():
                    if 'reduction' in metric.metric_type.lower():
                        score = min(metric.value, 100)
                    break
        
        # Check for zero waste commitments
        if brand.sustainability_commitments:
            commitments_text = str(brand.sustainability_commitments).lower()
            if 'zero waste' in commitments_text:
                score = max(score, 85.0)
            elif any(term in commitments_text for term in ['waste reduction', 'circular economy', 'recycling']):
                score = max(score, 70.0)
        
        return score
    
    async def _calculate_ethical_sourcing_score(self, brand: Brand, product: Optional[Product]) -> float:
        """Calculate ethical sourcing score."""
        
        score = 50.0
        
        # Check certifications
        if brand.certifications:
            ethical_certs = ['Fair Trade', 'Rainforest Alliance', 'B-Corp', 'B Corporation']
            for cert in brand.certifications:
                if any(c.lower() in cert.lower() for c in ethical_certs):
                    score = max(score, 85.0)
                    break
        
        # Check commitments
        if brand.sustainability_commitments:
            commitments_text = str(brand.sustainability_commitments).lower()
            if any(term in commitments_text for term in ['ethical sourcing', 'supply chain transparency', 'fair trade']):
                score = max(score, 75.0)
        
        return score
    
    async def _calculate_worker_rights_score(self, brand: Brand, product: Optional[Product]) -> float:
        """Calculate worker rights score."""
        
        score = 50.0
        
        # Check commitments
        if brand.sustainability_commitments:
            commitments_text = str(brand.sustainability_commitments).lower()
            if any(term in commitments_text for term in ['worker rights', 'fair labor', 'living wage', 'safe working conditions']):
                score = max(score, 75.0)
        
        # Check for B-Corp certification (implies worker rights focus)
        if brand.certifications:
            if any('b-corp' in cert.lower() or 'b corporation' in cert.lower() for cert in brand.certifications):
                score = max(score, 80.0)
        
        return score
    
    async def _calculate_community_impact_score(self, brand: Brand, product: Optional[Product]) -> float:
        """Calculate community impact score."""
        
        score = 50.0
        
        # Check commitments
        if brand.sustainability_commitments:
            commitments_text = str(brand.sustainability_commitments).lower()
            if any(term in commitments_text for term in ['community', 'local', 'social impact', 'giving back']):
                score = max(score, 70.0)
        
        return score
    
    async def _calculate_price_fairness_score(self, brand: Brand, product: Optional[Product]) -> float:
        """Calculate price fairness score."""
        
        # This would typically involve market analysis
        # For now, we'll use a simple heuristic
        score = 60.0  # Slightly above neutral
        
        # If Fair Trade certified, likely better price fairness
        if brand.certifications:
            if any('fair trade' in cert.lower() for cert in brand.certifications):
                score = max(score, 80.0)
        
        return score
    
    async def _calculate_durability_score(self, brand: Brand, product: Optional[Product]) -> float:
        """Calculate product durability score."""
        
        score = 50.0
        
        # Check product specifications for durability indicators
        if product and product.specifications:
            specs_text = str(product.specifications).lower()
            if any(term in specs_text for term in ['warranty', 'durable', 'lifetime', 'quality']):
                score = max(score, 70.0)
        
        # Check brand commitments for quality/durability focus
        if brand.sustainability_commitments:
            commitments_text = str(brand.sustainability_commitments).lower()
            if any(term in commitments_text for term in ['quality', 'durable', 'long-lasting', 'lifetime']):
                score = max(score, 65.0)
        
        return score
    
    def _estimate_renewable_energy_score(self, brand: Brand, nlp_analysis: Optional[Dict]) -> float:
        """Estimate renewable energy score from commitments."""
        
        score = 50.0
        
        if brand.sustainability_commitments:
            commitments_text = str(brand.sustainability_commitments).lower()
            if any(term in commitments_text for term in ['100% renewable', 'renewable energy', 'solar power', 'wind energy']):
                score = max(score, 80.0)
            elif 'renewable' in commitments_text:
                score = max(score, 70.0)
        
        return score
    
    def _calculate_confidence_score(self, 
                                  brand: Brand, 
                                  product: Optional[Product],
                                  nlp_analysis: Optional[Dict]) -> float:
        """Calculate confidence in the rating."""
        
        confidence = 0.0
        
        # Base confidence from data quality
        confidence += brand.data_quality_score * 0.3
        
        # Boost for certifications (more reliable)
        if brand.certifications:
            confidence += min(len(brand.certifications) * 0.1, 0.3)
        
        # Boost for quantitative metrics
        if brand.sustainability_metrics:
            confidence += min(len(brand.sustainability_metrics) * 0.05, 0.2)
        
        # Boost for NLP analysis quality
        if nlp_analysis:
            confidence += nlp_analysis.get('quality_score', 0) * 0.2
        
        return min(confidence, 1.0)
    
    def _calculate_data_completeness(self, brand: Brand, product: Optional[Product]) -> float:
        """Calculate how complete the data is."""
        
        completeness = 0.0
        
        # Check brand data completeness
        if brand.description:
            completeness += 0.1
        if brand.sustainability_commitments:
            completeness += 0.2
        if brand.certifications:
            completeness += 0.2
        if brand.sustainability_metrics:
            completeness += 0.3
        
        # Check product data if available
        if product:
            if product.description:
                completeness += 0.05
            if product.specifications:
                completeness += 0.1
            if product.materials:
                completeness += 0.05
        
        return min(completeness, 1.0)


class RatingCalculatorAgent(MCPAgent):
    """Rating Calculator Agent implementation."""
    
    def __init__(self):
        super().__init__(AgentRole.RATING_CALCULATOR, "Rating Calculator")
        
        self.nlp_analyzer = SustainabilityNLPAnalyzer()
        self.scorer = SustainabilityScorer()
        self.db = next(get_db())
        
        # Register message handlers
        self.register_handler("calculate_rating", self.calculate_rating)
        self.register_handler("recalculate_all_ratings", self.recalculate_all_ratings)
        self.register_handler("brand_data_updated", self.handle_brand_data_updated)
        self.register_handler("get_rating_history", self.get_rating_history)
        self.register_handler("update_rating_weights", self.update_rating_weights)
    
    async def initialize(self) -> bool:
        """Initialize the Rating Calculator agent."""
        logger.info("Initializing Rating Calculator Agent")
        
        try:
            # Test database connection
            self.db.execute("SELECT 1")
            
            logger.info("Rating Calculator Agent initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Rating Calculator: {e}")
            return False
    
    async def shutdown(self) -> None:
        """Shutdown the agent."""
        logger.info("Shutting down Rating Calculator Agent")
        self.db.close()
    
    async def calculate_rating(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate sustainability rating for a brand/product."""
        
        brand_id = params.get('brand_id')
        product_id = params.get('product_id')
        
        if not brand_id:
            raise ValueError("brand_id is required")
        
        logger.info(f"Calculating rating for brand {brand_id}, product {product_id}")
        
        try:
            # Get brand data
            brand = self.db.query(Brand).filter(Brand.id == brand_id).first()
            if not brand:
                return {'success': False, 'error': 'Brand not found'}
            
            # Get product data if specified
            product = None
            if product_id:
                product = self.db.query(Product).filter(Product.id == product_id).first()
                if not product:
                    return {'success': False, 'error': 'Product not found'}
            
            # Analyze commitments with NLP
            nlp_analysis = None
            if brand.sustainability_commitments:
                commitments = []
                if isinstance(brand.sustainability_commitments, dict):
                    commitments = brand.sustainability_commitments.get('commitments', [])
                elif isinstance(brand.sustainability_commitments, list):
                    commitments = brand.sustainability_commitments
                
                if commitments:
                    nlp_analysis = await self.nlp_analyzer.analyze_commitment_quality(commitments)
            
            # Calculate comprehensive score
            rating_components = await self.scorer.calculate_comprehensive_score(
                brand, product, nlp_analysis
            )
            
            # Calculate overall score
            overall_score = (
                rating_components.environmental_score * self.scorer.weights['environmental'] +
                rating_components.social_score * self.scorer.weights['social'] +
                rating_components.economic_score * self.scorer.weights['economic']
            )
            
            # Save rating to database
            rating_id = await self._save_rating(
                brand_id, product_id, overall_score, rating_components, nlp_analysis
            )
            
            # Notify other agents about new rating
            await self.send_notification(
                None,  # Broadcast to all agents
                "rating_calculated",
                {
                    'rating_id': rating_id,
                    'brand_id': brand_id,
                    'product_id': product_id,
                    'overall_score': overall_score,
                    'confidence_score': rating_components.confidence_score
                }
            )
            
            return {
                'success': True,
                'rating_id': rating_id,
                'overall_score': overall_score,
                'environmental_score': rating_components.environmental_score,
                'social_score': rating_components.social_score,
                'economic_score': rating_components.economic_score,
                'confidence_score': rating_components.confidence_score,
                'data_completeness': rating_components.data_completeness
            }
            
        except Exception as e:
            logger.error(f"Error calculating rating: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def recalculate_all_ratings(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Recalculate all ratings in the system."""
        
        logger.info("Recalculating all ratings")
        
        try:
            # Get all brands with products
            brands = self.db.query(Brand).all()
            
            results = {
                'success': True,
                'total_brands': len(brands),
                'calculated_ratings': 0,
                'errors': []
            }
            
            for brand in brands:
                try:
                    # Calculate rating for brand
                    result = await self.calculate_rating({'brand_id': brand.id})
                    if result['success']:
                        results['calculated_ratings'] += 1
                    else:
                        results['errors'].append(f"Brand {brand.id}: {result.get('error')}")
                    
                    # Calculate ratings for all products of this brand
                    for product in brand.products:
                        try:
                            result = await self.calculate_rating({
                                'brand_id': brand.id,
                                'product_id': product.id
                            })
                            if result['success']:
                                results['calculated_ratings'] += 1
                            else:
                                results['errors'].append(f"Product {product.id}: {result.get('error')}")
                        except Exception as e:
                            results['errors'].append(f"Product {product.id}: {str(e)}")
                            
                except Exception as e:
                    results['errors'].append(f"Brand {brand.id}: {str(e)}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error recalculating all ratings: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def handle_brand_data_updated(self, params: Dict[str, Any]) -> None:
        """Handle notification that brand data was updated."""
        
        brand_id = params.get('brand_id')
        if brand_id:
            logger.info(f"Brand data updated for brand {brand_id}, recalculating rating")
            await self.calculate_rating({'brand_id': brand_id})
    
    async def get_rating_history(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get rating history for a brand/product."""
        
        brand_id = params.get('brand_id')
        product_id = params.get('product_id')
        limit = params.get('limit', 10)
        
        try:
            query = self.db.query(SustainabilityRating)
            
            if product_id:
                query = query.filter(SustainabilityRating.product_id == product_id)
            elif brand_id:
                # Get ratings for all products of this brand
                query = query.join(Product).filter(Product.brand_id == brand_id)
            
            ratings = query.order_by(SustainabilityRating.created_at.desc()).limit(limit).all()
            
            history = []
            for rating in ratings:
                history.append({
                    'id': rating.id,
                    'overall_score': rating.overall_score,
                    'environmental_score': rating.environmental_score,
                    'social_score': rating.social_score,
                    'economic_score': rating.economic_score,
                    'confidence_score': rating.confidence_score,
                    'calculated_at': rating.calculated_at.isoformat(),
                    'algorithm_version': rating.algorithm_version
                })
            
            return {
                'success': True,
                'history': history
            }
            
        except Exception as e:
            logger.error(f"Error getting rating history: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def update_rating_weights(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update the weights used in rating calculations."""
        
        new_weights = params.get('weights', {})
        
        # Update main category weights
        if 'environmental' in new_weights:
            self.scorer.weights['environmental'] = new_weights['environmental']
        if 'social' in new_weights:
            self.scorer.weights['social'] = new_weights['social']
        if 'economic' in new_weights:
            self.scorer.weights['economic'] = new_weights['economic']
        
        # Normalize weights to sum to 1.0
        total = sum(self.scorer.weights.values())
        if total > 0:
            for key in self.scorer.weights:
                self.scorer.weights[key] /= total
        
        logger.info(f"Updated rating weights: {self.scorer.weights}")
        
        return {
            'success': True,
            'weights': self.scorer.weights
        }
    
    async def _save_rating(self, 
                          brand_id: int, 
                          product_id: Optional[int],
                          overall_score: float,
                          components: RatingComponents,
                          nlp_analysis: Optional[Dict]) -> int:
        """Save rating to database."""
        
        # Mark previous ratings as non-current
        if product_id:
            self.db.query(SustainabilityRating).filter(
                SustainabilityRating.product_id == product_id,
                SustainabilityRating.is_current == True
            ).update({'is_current': False})
        
        # Create new rating
        rating = SustainabilityRating(
            product_id=product_id,
            overall_score=overall_score,
            environmental_score=components.environmental_score,
            social_score=components.social_score,
            economic_score=components.economic_score,
            carbon_footprint_score=components.carbon_footprint_score,
            water_usage_score=components.water_usage_score,
            waste_reduction_score=components.waste_reduction_score,
            ethical_sourcing_score=components.ethical_sourcing_score,
            worker_rights_score=components.worker_rights_score,
            community_impact_score=components.community_impact_score,
            price_fairness_score=components.price_fairness_score,
            durability_score=components.durability_score,
            algorithm_version="1.0",
            confidence_score=components.confidence_score,
            data_completeness=components.data_completeness,
            factors_analyzed=['environmental', 'social', 'economic'],
            weights_used=self.scorer.weights,
            raw_metrics={'nlp_analysis': nlp_analysis} if nlp_analysis else {},
            expires_at=datetime.utcnow() + timedelta(days=30)  # Expire in 30 days
        )
        
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        
        return rating.id
