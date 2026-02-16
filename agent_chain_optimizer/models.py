"""
Data models for Agent Chain Optimizer
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime


@dataclass
class Agent:
    id: str
    name: str
    model: Optional[str] = None
    capabilities: Optional[List[str]] = None
    cost_per_token: Optional[Dict[str, float]] = None


@dataclass
class AgentStep:
    id: str
    agent_id: str
    agent_name: str
    dependencies: List[str] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    status: str = "pending"
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class Workflow:
    id: str
    name: str
    steps: List[AgentStep] = field(default_factory=list)
    total_latency: Optional[float] = None
    total_cost: Optional[float] = None
    success_rate: Optional[float] = None


@dataclass
class LatencyMetrics:
    p50: float
    p90: float
    p95: float
    p99: float
    mean: float
    min: float
    max: float
    std_dev: float
    variance: float


@dataclass
class QualityMetrics:
    success_rate: float
    failure_rate: float
    retry_count: int
    validation_pass_rate: Optional[float] = None


@dataclass
class ResourceMetrics:
    cpu_utilization: float
    memory_utilization: float
    gpu_utilization: Optional[float] = None
    peak_memory_mb: Optional[float] = None
    avg_memory_mb: Optional[float] = None


@dataclass
class StepAnalysis:
    step_id: str
    agent_id: str
    agent_name: str
    latency: float
    percentage_of_total: float
    is_bottleneck: bool
    cost: float
    success_rate: float
    optimization_recommendations: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CostBreakdown:
    step_id: str
    agent_id: str
    agent_name: str
    input_cost: float
    output_cost: float
    fixed_cost: float
    total_cost: float
    percentage: float


@dataclass
class PerformanceAnalysis:
    workflow_id: str
    total_latency: float
    latency_metrics: LatencyMetrics
    total_cost: float
    cost_breakdown: List[CostBreakdown]
    quality_metrics: QualityMetrics
    resource_metrics: ResourceMetrics
    step_analysis: List[StepAnalysis]
    timestamp: int


@dataclass
class CriticalPathStep:
    step_id: str
    agent_id: str
    agent_name: str
    start_time: int
    end_time: int
    duration: float
    dependencies: List[str]


@dataclass
class BottleneckStep:
    step_id: str
    agent_name: str
    latency: float
    impact_score: float
    cause: str


@dataclass
class OptimizationOpportunity:
    type: str
    steps: List[str]
    estimated_latency_reduction: float
    estimated_cost_reduction: float
    implementation_complexity: str


@dataclass
class CriticalPath:
    workflow_id: str
    steps: List[CriticalPathStep]
    total_latency: float
    bottleneck_steps: List[BottleneckStep]
    optimization_opportunities: List[OptimizationOpportunity]


@dataclass
class OptimizationResult:
    strategy_id: str
    type: str
    applied_at: int
    improvements: Dict[str, float]
    rollback_available: bool
    previous_config: Optional[Dict[str, Any]] = None
