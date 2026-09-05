from pydantic import BaseModel, ConfigDict, Field


class PipelineConfig(BaseModel):

    """

    Immutable configuration for one pipeline.


    Usage
    -----
    This model is a plain, frozen value object. As a library, the pipeline
    never reads environment variables or files at import time; the embedding
    application decides where values come from and passes them in explicitly.
    ```python
    from cvaugmentor import PipelineConfig

    config = PipelineConfig(verbose=True, random_state=True)
    ```

    """

    verbose: bool = Field(default=False, description="Whether the walk across a batch reports its progress")
    augmentation_verbose: bool = Field(default=False, description="Whether the work inside one medium reports its progress")
    warn_verbose: bool = Field(default=True, description="Whether skipped inputs are reported on the package logger")
    random_state: bool = Field(default=False, description="Whether every augmentation redraws its unspecified parameters between batch items")
    halt_on_error: bool = Field(default=False, description="Whether one unreadable medium aborts a batch instead of being recorded as skipped")

    model_config = ConfigDict(frozen=True)
