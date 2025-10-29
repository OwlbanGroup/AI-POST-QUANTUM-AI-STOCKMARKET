"""Google Gemini API integration for enhanced AI analysis."""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import google.generativeai as genai

logger = logging.getLogger(__name__)

class GeminiIntegration:
    """Google Gemini API integration for enhanced AI analysis"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini API integration

        Args:
            api_key: Google Gemini API key (optional, can be set via environment variable)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            logger.warning("No Gemini API key provided. Set GEMINI_API_KEY environment variable.")
            self.gemini_available = False
        else:
            genai.configure(api_key=self.api_key)
            self.gemini_available = True
            self.model = genai.GenerativeModel('gemini-pro')  # Default model

    def analyze_market_data(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Gemini to analyze market data and provide insights

        Args:
            market_data: Dictionary containing market data

        Returns:
            Dictionary with Gemini analysis results
        """
        if not self.gemini_available:
            return {"error": "Gemini API not available", "fallback": True}

        try:
            # Prepare market data for Gemini analysis
            prompt = self._create_market_analysis_prompt(market_data)

            # Generate response using Gemini API
            response = self.model.generate_content(prompt)
            analysis = self._parse_gemini_response(response.text)

            return {
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "model": "gemini-pro",
                "success": True
            }

        except (ValueError, Exception) as e:
            logger.error("Gemini analysis error: %s", e)
            return {"error": str(e), "fallback": True}

    def _create_market_analysis_prompt(self, market_data: Dict[str, Any]) -> str:
        """Create a comprehensive prompt for Gemini market analysis"""
        prompt = """Analyze the following stock market data and provide insights:

Market Data:
%s

Please provide:
1. Current market sentiment analysis
2. Key trends and patterns identified
3. Risk assessment and volatility analysis
4. Trading recommendations with confidence levels
5. Potential impact of external factors
6. Short-term and long-term outlook

Focus on:
- Technical analysis indicators
- Fundamental factors
- Market psychology
- Risk management considerations
- Blackwell-optimized AI processing capabilities

Provide analysis in a structured JSON format.
""" % json.dumps(market_data, indent=2)
        return prompt

    def _parse_gemini_response(self, response: str) -> Dict[str, Any]:
        """Parse Gemini CLI response into structured data"""
        try:
            # Try to parse as JSON first
            return json.loads(response)
        except json.JSONDecodeError:
            # If not JSON, structure the text response
            return {
                "raw_analysis": response,
                "sentiment": self._extract_sentiment(response),
                "recommendations": self._extract_recommendations(response),
                "confidence": self._estimate_confidence(response)
            }

    def _extract_sentiment(self, response: str) -> str:
        """Extract market sentiment from Gemini response"""
        response_lower = response.lower()
        if "bullish" in response_lower or "positive" in response_lower:
            return "bullish"
        elif "bearish" in response_lower or "negative" in response_lower:
            return "bearish"
        else:
            return "neutral"

    def _extract_recommendations(self, response: str) -> List[str]:
        """Extract trading recommendations from Gemini response"""
        recommendations = []
        lines = response.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'consider', 'buy', 'sell', 'hold']):
                recommendations.append(line.strip())
        return recommendations[:5]  # Limit to top 5 recommendations

    def _estimate_confidence(self, response: str) -> float:
        """Estimate confidence level from Gemini response"""
        confidence_indicators = {
            "high confidence": 0.9,
            "confident": 0.8,
            "moderate": 0.6,
            "low confidence": 0.4,
            "uncertain": 0.3
        }

        response_lower = response.lower()
        for indicator, score in confidence_indicators.items():
            if indicator in response_lower:
                return score

        return 0.7  # Default confidence

    def enhance_predictions(self, predictions: Dict[str, Any], market_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance existing AI predictions with Gemini insights

        Args:
            predictions: Existing model predictions
            market_context: Additional market context

        Returns:
            Enhanced predictions with Gemini insights
        """
        if not self.gemini_available:
            return predictions

        try:
            # Combine predictions with market context for Gemini analysis
            combined_data = {
                "predictions": predictions,
                "market_context": market_context,
                "timestamp": datetime.now().isoformat()
            }

            gemini_insights = self.analyze_market_data(combined_data)

            # Merge Gemini insights with existing predictions
            enhanced_predictions = {
                **predictions,
                "gemini_insights": gemini_insights,
                "enhanced": True,
                "enhancement_timestamp": datetime.now().isoformat()
            }

            return enhanced_predictions

        except (ValueError, Exception) as e:
            logger.error("Failed to enhance predictions with Gemini: %s", e)
            return predictions

    def get_market_sentiment(self, symbol: str, timeframe: str = "1D") -> Dict[str, Any]:
        """
        Get market sentiment analysis for a specific symbol

        Args:
            symbol: Stock symbol
            timeframe: Analysis timeframe

        Returns:
            Sentiment analysis results
        """
        if not self.gemini_available:
            return {"error": "Gemini not available", "symbol": symbol}

        prompt = """Analyze the market sentiment for %s over the %s timeframe.

Please provide:
1. Overall sentiment (bullish/bearish/neutral)
2. Key drivers of current sentiment
3. Sentiment strength (1-10 scale)
4. Potential catalysts for sentiment change
5. Risk factors to consider

Be specific to %s and consider both technical and fundamental factors.
""" % (symbol, timeframe, symbol)

        try:
            # Generate response using Gemini API
            response = self.model.generate_content(prompt)

            return {
                "symbol": symbol,
                "timeframe": timeframe,
                "sentiment_analysis": response.text.strip(),
                "timestamp": datetime.now().isoformat(),
                "success": True
            }

        except (ValueError, Exception) as e:
            return {"error": str(e), "symbol": symbol}

    def is_available(self) -> bool:
        """Check if Gemini integration is available"""
        return self.gemini_available
