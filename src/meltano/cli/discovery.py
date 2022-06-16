"""Discoverable Plugins CLI."""

from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from meltano.core.hub import MeltanoHubService
from meltano.core.hub.schema import IndexedPlugin
from meltano.core.legacy_tracking import LegacyTracker
from meltano.core.plugin import PluginType
from meltano.core.project import Project

from . import cli
from .params import pass_project


def _construct_table() -> Table:
    table = Table(title="MeltanoHub Plugins")
    table.add_column("Name", style="bold")
    table.add_column("Type", style="magenta")
    table.add_column("Variant Name", style="italic")
    table.add_column("Notes")
    table.add_column("MeltanoHub Link", style="cyan")

    return table


def _add_rows_rows(
    table: Table,
    plugin_type: PluginType,
    plugins: dict[str, IndexedPlugin],
):
    for plugin_name, plugin in plugins.items():
        for variant_name in plugin.variants:
            table.add_row(
                plugin_name,
                plugin_type.descriptor,
                variant_name,
                (
                    "[green]Default variant[/]"
                    if variant_name == plugin.default_variant
                    else ""
                ),
                f"https://hub.meltano.com/{plugin_type}/{plugin_name}--{variant_name}",
            )


@cli.command(short_help="List the available plugins in Meltano Hub and their variants.")
@click.argument(
    "plugin_type", type=click.Choice([*list(PluginType), "all"]), default="all"
)
@pass_project()
def discover(project: Project, plugin_type: str):
    """
    List the available discoverable plugins and their variants.

    \b\nRead more at https://docs.meltano.com/reference/command-line-interface#discover
    """
    hub_service = MeltanoHubService(project)
    console = Console()

    if plugin_type == "all":
        plugin_types = [
            plugin_type for plugin_type in list(PluginType) if plugin_type.discoverable
        ]
    else:
        plugin_types = [PluginType.from_cli_argument(plugin_type)]

    table = _construct_table()

    for idx, discovered_plugin_type in enumerate(plugin_types):
        if idx > 0:
            click.echo()

        try:
            plugin_type_index = hub_service.get_plugins_of_type(discovered_plugin_type)
        except Exception:
            click.secho(
                f"Can not retrieve {discovered_plugin_type} from the Hub",
                fg="yellow",
                err=True,
            )
            continue

        _add_rows_rows(table, discovered_plugin_type, plugin_type_index)

    with console.pager(styles=True):
        console.print(table)

    tracker = LegacyTracker(project)
    tracker.track_meltano_discover(plugin_type=plugin_type)
