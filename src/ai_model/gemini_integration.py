import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import subprocess
import tempfile

logger = logging.getLogger(__name__)

class GeminiIntegration:
    """Google Gemini CLI integration for enhanced AI analysis"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini CLI integration

        Args:
            api_key: Google Gemini API key (optional, can be set via environment variable)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            logger.warning("No Gemini API key provided. Set GEMINI_API_KEY environment variable.")

        self.gemini_available = self._check_gemini_availability()
        self.model = "gemini-pro"  # Default model

    def _check_gemini_availability(self) -> bool:
        """Check if Gemini CLI is available and properly configured"""
        try:
            result = subprocess.run(
                ["gemini", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning("Gemini CLI not available")
            return False

    def analyze_market_data(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Gemini to analyze market data and provide insights

        Args:
            market_data: Dictionary containing market data

        Returns:
            Dictionary with Gemini analysis results
        """
        if not self.gemini_available:
            return {"error": "Gemini CLI not available", "fallback": True}

        try:
            # Prepare market data for Gemini analysis
            prompt = self._create_market_analysis_prompt(market_data)

            # Create temporary file for prompt
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(prompt)
                prompt_file = f.name

            # Run Gemini CLI analysis
            result = subprocess.run(
                ["gemini", "analyze", "--model", self.model, "--file", prompt_file],
                capture_output=True,
                text=True,
                timeout=30,
                env={**os.environ, "GEMINI_API_KEY": self.api_key} if self.api_key else os.environ
            )

            # Clean up temporary file
            os.unlink(prompt_file)

            if result.returncode == 0:
                analysis = self._parse_gemini_response(result.stdout)
                return {
                    "analysis": analysis,
                    "timestamp": datetime.now().isoformat(),
                    "model": self.model,
                    "success": True
                }
            else:
                logger.error(f"Gemini analysis failed: {result.stderr}")
                return {"error": result.stderr, "fallback": True}

        except subprocess.TimeoutExpired:
            logger.error("Gemini analysis timed out")
            return {"error": "Analysis timed out", "fallback": True}
        except Exception as e:
            logger.error(f"Gemini analysis error: {e}")
            return {"error": str(e), "fallback": True}

    def _create_market_analysis_prompt(self, market_data: Dict[str, Any]) -> str:
        """Create a comprehensive prompt for Gemini market analysis"""
        prompt = f"""Analyze the following stock market data and provide insights:

Market Data:
{json.dumps(market_data, indent=2)}

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
"""
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

        except Exception as e:
            logger.error(f"Failed to enhance predictions with Gemini: {e}")
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

        prompt = f"""Analyze the market sentiment for {symbol} over the {timeframe} timeframe.

Please provide:
1. Overall sentiment (bullish/bearish/neutral)
2. Key drivers of current sentiment
3. Sentiment strength (1-10 scale)
4. Potential catalysts for sentiment change
5. Risk factors to consider

Be specific to {symbol} and consider both technical and fundamental factors.
"""

        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(prompt)
                prompt_file = f.name

            result = subprocess.run(
                ["gemini", "query", "--model", self.model, "--file", prompt_file],
                capture_output=True,
                text=True,
                timeout=20,
                env={**os.environ, "GEMINI_API_KEY": self.api_key} if self.api_key else os.environ
            )

            os.unlink(prompt_file)

            if result.returncode == 0:
                return {
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "sentiment_analysis": result.stdout.strip(),
                    "timestamp": datetime.now().isoformat(),
                    "success": True
                }
            else:
                return {"error": result.stderr, "symbol": symbol}

        except Exception as e:
            return {"error": str(e), "symbol": symbol}

    def is_available(self) -> bool:
        """Check if Gemini integration is available"""
        return self.gemini_available
