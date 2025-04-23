"""This module contains the function's business logic.

Use the automation_context module to wrap your function in an Automate context helper.
"""

from pydantic import Field
from speckle_automate import (
    AutomateBase,
    AutomationContext,
    execute_automate_function,
)

from specklepy.core.api.models import Version
from utils.traverse_utils import traverse_transform_data


class FunctionInputs(AutomateBase):
    """These are function author-defined values.

    Automate will make sure to supply them matching the types specified here.
    Please use the pydantic model schema to define your inputs:
    https://docs.pydantic.dev/latest/usage/models/
    """

    lat: float = Field(
        title="Latitude",
        description=(
            "Latitude (in degrees) of the selected location."
        ),
    )
    lon: float = Field(
        title="Longitude",
        description=(
            "Longitude (in degrees) of the selected location."
        ),
    )


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:
    """This is a Speckle Automate function reprojecting QGIS data to be compatible with CAD and BIM data.

    Args:
        automate_context: A context-helper object that carries relevant information
            about the runtime context of this function.
            It gives access to the Speckle project data that triggered this run.
            It also has convenient methods for attaching result data to the Speckle model.
        function_inputs: An instance object matching the defined schema.
    """

    # verify that it's a QGIS data
    version: Version = automate_context.speckle_client.version.get(automate_context.automation_run_data.triggers[0].payload.version_id, automate_context.automation_run_data.project_id)
    if version.sourceApplication.lower() != "qgis":
        automate_context.mark_run_failed(
        "Automation failed: "
        f"Source application {version.sourceApplication} is not supported for this function."
        )

    version_root_object = automate_context.receive_version()
    traverse_transform_data(version_root_object, function_inputs)

    automate_context.create_new_version_in_project(version_root_object, "local_gis_data")

    automate_context.mark_run_success("Data successfully reprojected.")
    return

    # If the function generates file results, this is how it can be
    # attached to the Speckle project/model
    # automate_context.store_file_result("./report.pdf")


def automate_function_without_inputs(automate_context: AutomationContext) -> None:
    """A function example without inputs.

    If your function does not need any input variables,
     besides what the automation context provides,
     the inputs argument can be omitted.
    """
    pass


# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference; do not invoke it!

    # Pass in the function reference with the inputs schema to the executor.
    execute_automate_function(automate_function, FunctionInputs)

    # If the function has no arguments, the executor can handle it like so
    # execute_automate_function(automate_function_without_inputs)
