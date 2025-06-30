# Brand Identity Management Workflow

A comprehensive system for automating brand identity creation and marketing campaign development using AI.

## 🎯 Quick Start (Recommended)

**For immediate use without any setup:**

1. **Download** `simple_brand_gui.html`
2. **Double-click** to open in your browser
3. **Enter your OpenAI API key** (get one from [OpenAI Platform](https://platform.openai.com/api-keys))
4. **Fill in your brand details** and click "Generate"

That's it! No installation, no dependencies, no setup required.

### What You Get
- ✅ **Brand Personality** (3-4 key traits)
- ✅ **Color Palette** (5-6 colors with hex codes)
- ✅ **Typography Suggestions** (2-3 font combinations)
- ✅ **Logo Concepts** (3 different style directions)
- ✅ **Brand Voice** (tone and messaging style)
- ✅ **Visual Style Guide** (key visual elements)

**Cost:** ~$0.02-0.05 per generation

---

## 🏗️ Advanced System (Multi-Agent Workflow)

For more complex workflows with multiple AI agents, see the full CrewAI-based system below.

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd brand_identity_workflow
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the workflow**
   ```bash
   python main.py
   ```

## 📋 Usage

### Simple HTML Interface (Recommended)

Just open `simple_brand_gui.html` in your browser and start generating brand identities immediately.

### Advanced Multi-Agent System

The system comes with a sample brand brief for "InnovateTech" - an AI software development company. Simply run:

```bash
python main.py
```

### Custom Brand Brief

To use your own brand, modify the `create_sample_brand_brief()` method in `main.py` or pass a custom brand brief:

```python
from main import BrandIdentityWorkflow

workflow = BrandIdentityWorkflow()

custom_brief = {
    'brand_name': 'YourBrand',
    'industry': 'Your Industry',
    'target_audience': 'Description of your target audience',
    'brand_values': ['Value1', 'Value2', 'Value3'],
    'style_preference': 'modern',  # modern, classic, minimalist, etc.
    'desired_mood': 'innovative',  # innovative, trustworthy, energetic, calming
    'brand_voice': 'professional yet approachable',
    'mission': 'Your brand mission',
    'vision': 'Your brand vision',
    'marketing_goals': ['Goal1', 'Goal2', 'Goal3']
}

results = workflow.run_complete_workflow(custom_brief)
```

## 🛠️ Technical Details

### Simple HTML Solution
- **Technology**: Pure HTML/CSS/JavaScript
- **Dependencies**: None (runs in browser)
- **Setup Time**: 0 seconds
- **File Size**: ~9KB
- **Deployment**: Just open the file

### Advanced Multi-Agent System
- **Framework**: CrewAI for multi-agent orchestration
- **Language**: Python 3.8+
- **AI Models**: OpenAI GPT models (configurable)
- **Storage**: JSON-based results storage
- **APIs**: Extensible tool system for external integrations

### File Structure

```
brand_identity_workflow/
├── simple_brand_gui.html    # 🎯 Quick start solution
├── main.py                  # Advanced orchestrator
├── agents.py                # Agent definitions
├── tasks.py                 # Task definitions
├── tools.py                 # Tool implementations
├── requirements.txt         # Dependencies
├── README.md               # Documentation
└── results/                # Generated outputs
    └── workflow_results_*.json
```

## 🔧 Configuration

### Simple HTML Solution
No configuration needed! Just get an OpenAI API key and start using.

### Advanced System

#### Environment Variables

Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
# Add other API keys as needed
```

#### Customizing Tools

To integrate with real APIs, modify the tools in `tools.py`:

```python
# Example: Real DALL-E integration
def generate_logo_concepts(brand_name, industry, target_audience, brand_values, style_preference):
    # Replace dummy implementation with actual API calls
    response = openai.Image.create(
        prompt=f"Logo design for {brand_name} in {industry}",
        n=3,
        size="1024x1024"
    )
    return response
```

## 📊 Output Examples

### Simple HTML Output
The HTML interface generates comprehensive brand identity recommendations including:
- Brand personality traits
- Color palettes with hex codes
- Typography suggestions
- Logo concept descriptions
- Brand voice guidelines
- Visual style recommendations

### Advanced System Output

```json
{
  "brand_identity": {
    "logo_concepts": {
      "concepts_count": 3,
      "status": "generated",
      "concepts": [
        {
          "id": "concept_1",
          "name": "InnovateTech_modern_minimal",
          "description": "Modern, minimalist logo",
          "rationale": "Clean design reflecting modern aesthetic",
          "file_path": "assets/logos/InnovateTech_concept_1.png"
        }
      ]
    },
    "color_palette": {
      "palette_type": "comprehensive",
      "colors_count": 4,
      "palette": {
        "primary": {"hex": "#1A365D", "usage": "Main brand color"},
        "secondary": {"hex": "#2D3748", "usage": "Supporting elements"},
        "accent": {"hex": "#3182CE", "usage": "Highlights and CTAs"},
        "neutral": {"hex": "#E2E8F0", "usage": "Backgrounds"}
      }
    }
  }
}
```

## 🎨 Brand Templates

The system generates comprehensive brand templates including:

### Visual Style Guide
- Brand overview and positioning
- Logo usage guidelines
- Color specifications
- Typography guidelines
- Imagery style standards
- Digital and print guidelines

### Marketing Templates
- Social media post templates
- Email campaign sequences
- Video script templates
- Content calendar structures

## 🚀 Future Enhancements

### Planned Features
- **Real API Integration**: DALL-E, Midjourney, social media APIs
- **Web Interface**: User-friendly dashboard for workflow management
- **Database Integration**: PostgreSQL for persistent storage
- **Advanced Analytics**: Performance tracking and optimization
- **Custom Brand Briefs**: Web form for brand input
- **Export Formats**: PDF, HTML, and design file exports

### Extensibility
- **Plugin System**: Easy addition of new tools and agents
- **Custom Workflows**: Configurable workflow sequences
- **Multi-language Support**: International brand development
- **Industry Specialization**: Industry-specific templates and guidelines

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

## 🙏 Acknowledgments

- CrewAI team for the multi-agent framework
- OpenAI for AI model capabilities
- The design and marketing communities for best practices

---

**Note**: The simple HTML solution is ready for immediate use. The advanced system is a demonstration and requires integration with real APIs for production use. 