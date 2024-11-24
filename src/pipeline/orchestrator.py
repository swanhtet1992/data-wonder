"""Pipeline orchestrator for document processing and question generation."""
from typing import Optional, List, Dict, Any
from .types import (
    ProcessingConfig, GenerationConfig, DocumentChunk, 
    PipelineResult, ProgressCallback, Question
)
from .processors.document_processor import DocumentProcessor
from .generators.question_generator import QuestionGenerator
from .generators.answer_generator import AnswerGenerator

class PipelineOrchestrator:
    """Orchestrates the document processing and question generation pipeline."""
    
    def __init__(self, 
                 document_processor: DocumentProcessor,
                 question_generator: QuestionGenerator,
                 answer_generator: AnswerGenerator):
        """Initialize orchestrator with required components."""
        self.document_processor = document_processor
        self.question_generator = question_generator
        self.answer_generator = answer_generator
    
    async def generate_questions(self,
                               content: str,
                               processing_config: Optional[ProcessingConfig] = None,
                               generation_config: Optional[GenerationConfig] = None,
                               progress_callback: Optional[ProgressCallback] = None
                               ) -> List[Dict[str, Any]]:
        """Generate questions without answers."""
        try:
            if progress_callback:
                progress_callback(0.1, "Processing document...")
            
            # Process document into chunks
            chunks = self.document_processor.chunk_document(
                content,
                max_chunk_size=processing_config.max_chunk_size if processing_config else 2000,
                overlap_tokens=processing_config.overlap_tokens if processing_config else 64
            )
            
            if progress_callback:
                progress_callback(0.4, "Generating questions...")
            
            # Generate questions
            questions = await self.question_generator.generate(
                input_data=content,
                config={
                    "questions_per_chunk": generation_config.questions_per_chunk if generation_config else 3,
                    "temperature": generation_config.temperature if generation_config else 0.7,
                    "max_tokens": generation_config.max_tokens if generation_config else 1000,
                    "quality_threshold": generation_config.quality_threshold if generation_config else 0.7,
                }
            )
            
            if progress_callback:
                progress_callback(1.0, "Questions generated!")
                
            return questions
            
        except Exception as e:
            raise Exception(f"Question generation failed: {str(e)}")
    
    async def generate_answers(self,
                             questions: List[Dict[str, Any]],
                             context: str,
                             generation_config: Optional[GenerationConfig] = None,
                             progress_callback: Optional[ProgressCallback] = None
                             ) -> List[Question]:
        """Generate answers for existing questions."""
        try:
            answers = []
            total = len(questions)
            
            for idx, question in enumerate(questions):
                if progress_callback:
                    progress = idx / total
                    progress_callback(progress, f"Generating answer {idx + 1}/{total}")
                
                answer = await self.answer_generator.generate(
                    input_data={
                        "question": question["question"],
                        "context": context
                    },
                    config={
                        "temperature": generation_config.temperature if generation_config else 0.7,
                        "max_tokens": generation_config.max_tokens if generation_config else 1000,
                        "quality_threshold": generation_config.quality_threshold if generation_config else 0.7,
                    }
                )
                
                # Combine question and answer data
                qa_pair = {
                    **question,
                    **answer
                }
                answers.append(qa_pair)
            
            if progress_callback:
                progress_callback(1.0, "Answers generated!")
                
            return answers
            
        except Exception as e:
            raise Exception(f"Answer generation failed: {str(e)}")