"""
Client for Agent Chain Optimizer
"""

import requests
from typing import Dict, List, Optional, Any
from .models import (
    Workflow,
    Agent,
    AgentStep,
    PerformanceAnalysis,
    CriticalPath,
    OptimizationResult,
)


class OptimizerClient:
    """Python client for Agent Chain Optimizer API"""
    
    def __init__(self, base_url: str = "http://localhost:3000/api/optimizer"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def analyze_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Analyze a workflow by ID"""
        response = self.session.post(
            f"{self.base_url}/analyze",
            json={"workflowId": workflow_id}
        )
        response.raise_for_status()
        return response.json()
    
    def optimize_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize a workflow"""
        response = self.session.post(
            f"{self.base_url}/optimize",
            json={"workflow": workflow}
        )
        response.raise_for_status()
        return response.json()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get aggregated metrics"""
        response = self.session.get(f"{self.base_url}/metrics")
        response.raise_for_status()
        return response.json()
    
    def get_critical_path(self, execution_id: str) -> Dict[str, Any]:
        """Get critical path for an execution"""
        response = self.session.get(
            f"{self.base_url}/critical-path/{execution_id}"
        )
        response.raise_for_status()
        return response.json()
    
    def create_workflow(
        self,
        workflow_id: str,
        name: str,
        steps: List[Dict[str, Any]],
        agents: Optional[List[Dict[str, Any]]] = None
    ) -> Workflow:
        """Create a workflow locally (for offline use)"""
        workflow_steps = [
            AgentStep(
                id=step.get("id", f"step-{i}"),
                agent_id=step.get("agentId", step.get("agent_id")),
                agent_name=step.get("agentName", step.get("agent_name", "Unknown")),
                dependencies=step.get("dependencies", []),
                input_tokens=step.get("inputTokens", step.get("input_tokens", 0)),
                output_tokens=step.get("outputTokens", step.get("output_tokens", 0)),
            )
            for i, step in enumerate(steps)
        ]
        
        return Workflow(
            id=workflow_id,
            name=name,
            steps=workflow_steps,
        )
    
    def calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        input_cost_per_1k: float = 0.001,
        output_cost_per_1k: float = 0.002
    ) -> float:
        """Calculate cost for token usage"""
        input_cost = (input_tokens / 1000) * input_cost_per_1k
        output_cost = (output_tokens / 1000) * output_cost_per_1k
        return input_cost + output_cost
    
    def close(self):
        """Close the session"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
