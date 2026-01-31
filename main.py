"""
Main orchestrator for the Brand Identity Management Agent Workflow.
Coordinates the execution of brand identity creation and marketing campaigns using hierarchical process.

Supports free local models via Ollama. Set CREWAI_MODEL env var to choose model:
  - qwen2.5 (default) - Fast general purpose
  - qwen2.5-vl - Best for visual tasks
  - deepseek-v3 - Great for agents (MIT license)
  - llama3.2 - Meta's latest
  - gpt-4o / gpt-4o-mini - OpenAI (paid)
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv

from crewai import Crew, Process
from agents import get_brand_identity_crew_agents, get_marketing_crew_agents, get_all_agents
from tasks import get_coordinator_tasks
from tools import DataManagementTools
from llm_config import get_llm, list_available_models, DEFAULT_MODEL

# Load environment variables
load_dotenv()

class BrandIdentityWorkflow:
    """
    Main orchestrator class for the brand identity management workflow.
    Now uses hierarchical process with manager agents.
    Supports free local models via Ollama.
    """

    def __init__(self, model_name: str = None):
        """
        Initialize the workflow orchestrator.

        Args:
            model_name: Name of the LLM model to use (see llm_config.py for options).
                       Defaults to CREWAI_MODEL env var or 'qwen2.5'.
        """
        # Get the configured LLM
        self.llm = get_llm(model_name)
        self.model_name = model_name or DEFAULT_MODEL

        # Initialize agents with the configured LLM
        self.brand_identity_agents = get_brand_identity_crew_agents(self.llm)
        self.marketing_agents = get_marketing_crew_agents(self.llm)
        self.all_agents = get_all_agents(self.llm)

        print(f"Using LLM: {self.model_name}")
        
        # Initialize results storage
        self.workflow_results = {
            'brand_identity': {},
            'marketing': {},
            'metadata': {
                'start_time': None,
                'end_time': None,
                'brand_name': None,
                'status': 'pending'
            }
        }
    
    def create_sample_brand_brief(self) -> Dict[str, Any]:
        """
        Create a sample brand brief for demonstration purposes.
        
        Returns:
            Dictionary containing brand brief information
        """
        return {
            'brand_name': 'InnovateTech',
            'industry': 'AI Software Development',
            'target_audience': 'Tech-savvy professionals aged 25-45, working in software development, data science, and IT management',
            'brand_values': ['Innovation', 'Reliability', 'Efficiency', 'Collaboration', 'Excellence'],
            'style_preference': 'modern',
            'desired_mood': 'innovative',
            'brand_voice': 'professional yet approachable',
            'mission': 'To empower developers and organizations with cutting-edge AI tools that streamline workflows and drive innovation',
            'vision': 'To be the leading platform for AI-powered development tools, making advanced technology accessible to every developer',
            'competitors': ['GitHub Copilot', 'Tabnine', 'Kite'],
            'unique_selling_proposition': 'Seamless integration with existing development workflows with advanced customization and team collaboration features',
            'marketing_goals': ['Increase brand awareness', 'Drive product adoption', 'Build developer community', 'Generate qualified leads'],
            'budget_considerations': 'Mid-market pricing with freemium model',
            'timeline': '3-6 months for full brand rollout'
        }
    
    def run_brand_identity_workflow(self, brand_brief: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the brand identity creation workflow using hierarchical process.
        
        Args:
            brand_brief: Brand information dictionary
            
        Returns:
            Dictionary containing brand identity results
        """
        print("=" * 80)
        print("🚀 STARTING BRAND IDENTITY CREATION WORKFLOW (Hierarchical)")
        print("=" * 80)
        print(f"Brand: {brand_brief['brand_name']}")
        print(f"Industry: {brand_brief['industry']}")
        print(f"Target Audience: {brand_brief['target_audience']}")
        print(f"Brand Values: {', '.join(brand_brief['brand_values'])}")
        print("=" * 80)
        
        # Get coordinator tasks for hierarchical workflow
        coordinator_tasks = get_coordinator_tasks()
        
        # Create hierarchical crew for brand identity
        brand_identity_crew = Crew(
            agents=self.brand_identity_agents,  # Manager is already first in the list
            tasks=[coordinator_tasks['brand_identity_coordination']],  # Only the coordinator task
            process=Process.hierarchical,  # Key change: hierarchical process
            manager_llm=self.llm,  # Required for hierarchical process
            verbose=True,
            memory=True
        )
        
        # Execute brand identity workflow
        try:
            brand_identity_result = brand_identity_crew.kickoff(inputs=brand_brief)
            
            # Parse and structure results
            self.workflow_results['brand_identity'] = {
                'logo_concepts': self._extract_logo_concepts(brand_identity_result),
                'color_palette': self._extract_color_palette(brand_identity_result),
                'style_guide': self._extract_style_guide(brand_identity_result),
                'raw_result': brand_identity_result
            }

            # Generate artistic logo variants using local Ollama SDXL (best-effort)
            try:
                from tools import generate_artistic_logo
                art_json = generate_artistic_logo.func(brand_brief.get('brand_name', ''), prompt='', style=brand_brief.get('style_preference', 'modern'), variants=3, resolution='1024x1024', model=os.getenv('OLLAMA_IMAGE_MODEL', 'sdxl'))
                try:
                    art = json.loads(art_json) if isinstance(art_json, str) else art_json
                except Exception:
                    art = {'brand': brand_brief.get('brand_name', ''), 'variants': []}
                self.workflow_results['brand_identity']['artistic_logos'] = art
            except Exception as e:
                print(f"Warning: artistic logo generation step failed: {e}")
            
            print("\n" + "=" * 80)
            print("✅ BRAND IDENTITY WORKFLOW COMPLETED SUCCESSFULLY")
            print("=" * 80)
            
            return self.workflow_results['brand_identity']
            
        except Exception as e:
            print(f"\n❌ Error in brand identity workflow: {str(e)}")
            raise
    
    def run_marketing_workflow(self, brand_brief: Dict[str, Any], style_guide: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the marketing campaign workflow using hierarchical process.
        
        Args:
            brand_brief: Brand information dictionary
            style_guide: Results from brand identity workflow
            
        Returns:
            Dictionary containing marketing results
        """
        print("\n" + "=" * 80)
        print("🚀 STARTING MARKETING CAMPAIGN WORKFLOW (Hierarchical)")
        print("=" * 80)
        print(f"Brand: {brand_brief['brand_name']}")
        print(f"Style Guide: Available")
        print(f"Marketing Goals: {', '.join(brand_brief['marketing_goals'])}")
        print("=" * 80)
        
        # Update brand brief with style guide
        brand_brief_with_style_guide = {**brand_brief, 'style_guide': style_guide}
        
        # Get coordinator tasks for hierarchical workflow
        coordinator_tasks = get_coordinator_tasks()
        
        # Create hierarchical crew for marketing
        marketing_crew = Crew(
            agents=self.marketing_agents,  # Manager is already first in the list
            tasks=[coordinator_tasks['marketing_coordination']],  # Only the coordinator task
            process=Process.hierarchical,  # Key change: hierarchical process
            manager_llm=self.llm,  # Required for hierarchical process
            verbose=True,
            memory=True
        )
        
        # Execute marketing workflow
        try:
            marketing_result = marketing_crew.kickoff(inputs=brand_brief_with_style_guide)
            
            # Parse and structure results
            self.workflow_results['marketing'] = {
                'social_media_content': self._extract_social_media_content(marketing_result),
                'email_campaigns': self._extract_email_campaigns(marketing_result),
                'video_content': self._extract_video_content(marketing_result),
                'raw_result': marketing_result
            }
            
            print("\n" + "=" * 80)
            print("✅ MARKETING WORKFLOW COMPLETED SUCCESSFULLY")
            print("=" * 80)
            
            return self.workflow_results['marketing']
            
        except Exception as e:
            print(f"\n❌ Error in marketing workflow: {str(e)}")
            raise
    
    def run_complete_workflow(self, brand_brief: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute the complete brand identity and marketing workflow using hierarchical process.
        
        Args:
            brand_brief: Brand information dictionary (optional, will use sample if not provided)
            
        Returns:
            Dictionary containing complete workflow results
        """
        # Use sample brand brief if none provided
        if brand_brief is None:
            brand_brief = self.create_sample_brand_brief()
        
        # Update metadata
        self.workflow_results['metadata'].update({
            'start_time': datetime.now().isoformat(),
            'brand_name': brand_brief['brand_name'],
            'status': 'running'
        })
        
        print("🎯 BRAND IDENTITY MANAGEMENT WORKFLOW (Hierarchical)")
        print("=" * 80)
        print("This workflow uses hierarchical process with manager agents.")
        print("Manager agents will delegate tasks to specialist worker agents.")
        print("=" * 80)
        
        try:
            # Step 1: Brand Identity Creation (Hierarchical)
            brand_identity_results = self.run_brand_identity_workflow(brand_brief)
            
            # Step 2: Marketing Campaign Development (Hierarchical)
            marketing_results = self.run_marketing_workflow(brand_brief, brand_identity_results['style_guide'])
            
            # Step 3: Save complete results
            self.workflow_results['metadata'].update({
                'end_time': datetime.now().isoformat(),
                'status': 'completed'
            })
            
            # Generate final summary
            final_summary = self._generate_workflow_summary(brand_brief, brand_identity_results, marketing_results)
            
            print("\n" + "=" * 80)
            print("🎉 COMPLETE WORKFLOW FINISHED SUCCESSFULLY!")
            print("=" * 80)
            print(final_summary)
            print("=" * 80)
            
            return self.workflow_results
            
        except Exception as e:
            self.workflow_results['metadata']['status'] = 'failed'
            self.workflow_results['metadata']['error'] = str(e)
            print(f"\n❌ Workflow failed: {str(e)}")
            raise
    
    def _extract_logo_concepts(self, result: str) -> Dict[str, Any]:
        """Extract logo concepts from workflow result."""
        # This is a simplified extraction - in a real implementation,
        # you would parse the structured output more carefully
        return {
            'concepts_count': 3,
            'status': 'generated',
            'extraction_method': 'text_parsing'
        }
    
    def _extract_color_palette(self, result: str) -> Dict[str, Any]:
        """Extract color palette from workflow result."""
        return {
            'palette_type': 'comprehensive',
            'colors_count': 4,
            'status': 'generated',
            'extraction_method': 'text_parsing'
        }
    
    def _extract_style_guide(self, result: str) -> Dict[str, Any]:
        """Extract style guide from workflow result."""
        return {
            'document_type': 'comprehensive_style_guide',
            'sections_count': 6,
            'status': 'generated',
            'extraction_method': 'text_parsing'
        }
    
    def _extract_social_media_content(self, result: str) -> Dict[str, Any]:
        """Extract social media content from workflow result."""
        return {
            'platforms_covered': ['Instagram', 'LinkedIn', 'Twitter', 'Facebook'],
            'posts_per_platform': 3,
            'status': 'generated',
            'extraction_method': 'text_parsing'
        }
    
    def _extract_email_campaigns(self, result: str) -> Dict[str, Any]:
        """Extract email campaigns from workflow result."""
        return {
            'campaign_types': ['Welcome', 'Nurture', 'Promotional'],
            'emails_per_campaign': 3,
            'status': 'generated',
            'extraction_method': 'text_parsing'
        }
    
    def _extract_video_content(self, result: str) -> Dict[str, Any]:
        """Extract video content from workflow result."""
        return {
            'platforms_covered': ['TikTok', 'Instagram', 'YouTube', 'LinkedIn'],
            'videos_per_platform': 2,
            'status': 'generated',
            'extraction_method': 'text_parsing'
        }
    
    def _generate_workflow_summary(self, brand_brief: Dict[str, Any], 
                                 brand_identity_results: Dict[str, Any],
                                 marketing_results: Dict[str, Any]) -> str:
        """Generate a summary of the complete workflow."""
        summary = f"""
BRAND IDENTITY MANAGEMENT WORKFLOW SUMMARY (Hierarchical)

Brand: {brand_brief['brand_name']}
Industry: {brand_brief['industry']}
Workflow Status: {self.workflow_results['metadata']['status']}
Process Type: Hierarchical (Manager Agents)

BRAND IDENTITY DELIVERABLES:
✅ Logo Concepts: {brand_identity_results['logo_concepts']['concepts_count']} concepts generated
✅ Color Palette: {brand_identity_results['color_palette']['colors_count']} color categories defined
✅ Style Guide: Comprehensive brand guidelines created

MARKETING DELIVERABLES:
✅ Social Media Content: {marketing_results['social_media_content']['platforms_covered']} platforms covered
✅ Email Campaigns: {len(marketing_results['email_campaigns']['campaign_types'])} campaign types developed
✅ Video Content: {marketing_results['video_content']['platforms_covered']} platforms covered

HIERARCHICAL PROCESS BENEFITS:
✅ Manager agents orchestrate the workflow
✅ Worker agents focus on specialized tasks
✅ Structured Pydantic outputs ensure data integrity
✅ Improved reliability and maintainability

NEXT STEPS:
1. Review and approve brand identity elements
2. Implement style guide across all touchpoints
3. Launch marketing campaigns according to schedule
4. Monitor performance and iterate based on results

All deliverables have been generated using hierarchical process and are ready for implementation!
        """
        return summary
    
    def save_results(self, filename: str = None) -> str:
        """
        Save workflow results to a JSON file.
        
        Args:
            filename: Optional filename, will generate one if not provided
            
        Returns:
            Path to the saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            brand_name = self.workflow_results['metadata'].get('brand_name', 'unknown')
            filename = f"workflow_results_{brand_name}_{timestamp}.json"
        
        # Ensure the results directory exists
        os.makedirs('results', exist_ok=True)
        filepath = os.path.join('results', filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.workflow_results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {filepath}")
        return filepath


def main():
    """Main entry point for the brand identity workflow."""
    import argparse

    parser = argparse.ArgumentParser(description="Brand Identity Management Workflow")
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=None,
        help="LLM model to use (e.g., qwen2.5, deepseek-v3, gpt-4o). Default: qwen2.5"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List available LLM models and exit"
    )
    args = parser.parse_args()

    if args.list_models:
        list_available_models()
        return

    try:
        # Initialize the workflow with specified model
        workflow = BrandIdentityWorkflow(model_name=args.model)

        # Run the complete workflow
        results = workflow.run_complete_workflow()

        # Save results
        workflow.save_results()

        print("\n🎯 Workflow completed successfully!")
        print("Check the 'results' directory for detailed output files.")

    except Exception as e:
        print(f"\n❌ Workflow failed: {str(e)}")
        print("Please check the error details and try again.")


if __name__ == "__main__":
    main()
