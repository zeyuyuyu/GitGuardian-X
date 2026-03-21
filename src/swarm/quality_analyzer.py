import ast
from typing import Dict, List, Optional
from dataclasses import dataclass
import numpy as np
from pathlib import Path

@dataclass
class QualityMetrics:
    cognitive_complexity: float
    maintainability_index: float
    documentation_ratio: float
    code_smells: List[str]
    suggested_improvements: List[str]

class CodeQualityAnalyzer:
    def __init__(self, model_path: Optional[str] = None):
        self.complexity_threshold = 15
        self.doc_ratio_threshold = 0.2
        self.metrics_cache: Dict[str, QualityMetrics] = {}

    def analyze_file(self, file_path: Path) -> QualityMetrics:
        """Analyzes a Python file for code quality metrics and suggests improvements."""
        if str(file_path) in self.metrics_cache:
            return self.metrics_cache[str(file_path)]

        with open(file_path, 'r') as f:
            content = f.read()

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return QualityMetrics(
                cognitive_complexity=float('inf'),
                maintainability_index=0.0,
                documentation_ratio=0.0,
                code_smells=['Invalid Python syntax'],
                suggested_improvements=['Fix syntax errors']
            )

        metrics = self._calculate_metrics(tree, content)
        self.metrics_cache[str(file_path)] = metrics
        return metrics

    def _calculate_metrics(self, tree: ast.AST, content: str) -> QualityMetrics:
        complexity = self._calculate_cognitive_complexity(tree)
        doc_ratio = self._calculate_documentation_ratio(tree, content)
        maintainability = self._calculate_maintainability_index(tree, content)
        
        code_smells = []
        improvements = []

        if complexity > self.complexity_threshold:
            code_smells.append(f'High cognitive complexity: {complexity}')
            improvements.append('Consider breaking down complex functions')

        if doc_ratio < self.doc_ratio_threshold:
            code_smells.append(f'Low documentation ratio: {doc_ratio:.2f}')
            improvements.append('Add more documentation to improve code clarity')

        return QualityMetrics(
            cognitive_complexity=complexity,
            maintainability_index=maintainability,
            documentation_ratio=doc_ratio,
            code_smells=code_smells,
            suggested_improvements=improvements
        )

    def _calculate_cognitive_complexity(self, tree: ast.AST) -> float:
        """Calculate cognitive complexity using AST analysis."""
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For)):
                complexity += 1
            elif isinstance(node, ast.FunctionDef):
                complexity += len([n for n in ast.walk(node) if isinstance(n, ast.Return)])
        return complexity

    def _calculate_documentation_ratio(self, tree: ast.AST, content: str) -> float:
        """Calculate the ratio of documentation to code."""
        doc_lines = sum(1 for node in ast.walk(tree) 
                       if isinstance(node, ast.Expr) and 
                       isinstance(node.value, ast.Str))
        total_lines = len(content.splitlines())
        return doc_lines / total_lines if total_lines > 0 else 0

    def _calculate_maintainability_index(self, tree: ast.AST, content: str) -> float:
        """Calculate maintainability index using standard formula."""
        lines = len(content.splitlines())
        complexity = self._calculate_cognitive_complexity(tree)
        unique_operators = len(set(node.__class__.__name__ 
                                 for node in ast.walk(tree)))

        # Simplified maintainability index formula
        mi = 100 - (complexity * 0.2) - (lines * 0.1) - (unique_operators * 0.2)
        return max(0.0, min(100.0, mi))

    def get_quality_score(self, metrics: QualityMetrics) -> float:
        """Calculate overall quality score from metrics."""
        weights = {
            'complexity': 0.4,
            'maintainability': 0.3,
            'documentation': 0.3
        }

        complexity_score = max(0, 1 - (metrics.cognitive_complexity / 
                                      (2 * self.complexity_threshold)))
        
        return (
            weights['complexity'] * complexity_score +
            weights['maintainability'] * (metrics.maintainability_index / 100) +
            weights['documentation'] * min(1, metrics.documentation_ratio / 
                                         self.doc_ratio_threshold)
        )
