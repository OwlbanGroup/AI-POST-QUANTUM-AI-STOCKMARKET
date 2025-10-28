# AI Post Quantum AI Stockmarket

This project aims to develop an AI-driven stock market analysis tool that incorporates post-quantum computing principles. The application will leverage advanced AI algorithms to analyze stock market data and provide insights.

## NVIDIA Blackwell Architecture Integration

This project now includes end-to-end integration with NVIDIA Blackwell architecture for enhanced performance:

### Blackwell Optimizations

- **GPU Acceleration**: RAPIDS cuDF for high-performance data processing
- **TensorRT Integration**: Blackwell-optimized inference with FP16 precision and sparse weights
- **CUDA 12.4 Support**: Latest CUDA toolkit with Blackwell-specific optimizations
- **Containerized Deployment**: NVIDIA CUDA runtime base image for seamless deployment

### Hardware Requirements

- NVIDIA GPU with Blackwell architecture (compute capability 9.x+)
- CUDA 12.4 compatible drivers
- Minimum 8GB GPU memory recommended

### Blackwell-Specific Features

- Automatic architecture detection and optimization
- Enhanced TensorRT configurations for Blackwell
- RAPIDS ecosystem integration (cuML, cuGraph, cuSpatial)
- PyTorch with CUDA 12.4 support

## Google Gemini AI Integration

The project now includes Google Gemini CLI integration for enhanced AI-driven market analysis:

### Gemini Features

- **Market Sentiment Analysis**: Real-time sentiment analysis using Gemini AI
- **Enhanced Predictions**: AI-powered insights complementing traditional ML models
- **Intelligent Recommendations**: Context-aware trading recommendations
- **Risk Assessment**: Advanced risk evaluation with AI insights

### Gemini Setup

1. Install Google Gemini CLI:

   ```bash
   pip install google-gemini-cli
   ```

2. Set your API key:

   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

3. The system automatically detects and integrates Gemini capabilities

### Gemini-Enhanced Features

- Automatic market data analysis with Gemini insights
- Enhanced prediction confidence through AI analysis
- Intelligent market sentiment tracking
- Blackwell-optimized Gemini processing pipeline

## Project Structure

## Deployment Instructions

### Standard Deployment

To deploy the application, follow these steps:

1. Ensure all dependencies are installed:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:

   ```bash
   python src/main.py
   ```

3. Access the application in your web browser at `http://localhost:5000`.

### Blackwell GPU Deployment

For Blackwell-optimized deployment:

1. Build the Docker image:

   ```bash
   docker build -t ai-stockmarket-blackwell .
   ```

2. Run with GPU support:

   ```bash
   docker run --gpus all -p 5000:5000 ai-stockmarket-blackwell
   ```

3. Verify Blackwell optimizations are active in the application logs.

### Environment Setup

- `src/`: Contains the source code for the application.
- `requirements.txt`: Lists the dependencies required for the project, including Blackwell-specific packages.
- `Dockerfile`: NVIDIA CUDA 12.4 runtime base image for Blackwell compatibility.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `TODO_BLACKWELL_INTEGRATION.md`: Blackwell integration roadmap and status.
