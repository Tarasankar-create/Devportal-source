from pydantic import BaseModel, Field
from typing import Optional,Annotated
from datetime import datetime,timezone

class JenkinsEvent(BaseModel):
    project: Annotated[str, Field(..., description="The name of the Jenkins project.")]
    build_number: Annotated[int, Field(..., description="The build number of the Jenkins project.")]
    status: Annotated[str, Field(..., description="The status of the Jenkins build.")]
    image_tag: Optional[Annotated[str, Field(None, description="The image tag associated with the Jenkins build.")]] = None
    timestamp: Annotated[datetime, Field(default_factory=datetime.now(timezone.utc), description="The timestamp when the event was created.")]

class ArgoCDEvent(BaseModel):
    application: Annotated[str, Field(..., description="The name of the Argo CD application.")]
    sync_status: Annotated[str, Field(..., description="The synchronization status of the Argo CD application.")]
    revision: Optional[Annotated[str, Field(None, description="The revision of the Argo CD application.")]] = None
    timestamp: Annotated[datetime, Field(datetime.now(timezone.utc), description="The timestamp when the event was created.")]