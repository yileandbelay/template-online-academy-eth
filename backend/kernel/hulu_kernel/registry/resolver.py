"""Resolve a product's blocks: versions present, capabilities provided, no cycles, load order (spec 6.2, 12)."""

from __future__ import annotations

from collections.abc import Iterable

from hulu_kernel.registry.manifest import BlockManifest, ProductManifest


class ResolutionError(Exception):
    """The product cannot be assembled. The message says what to change."""


def resolve(
    product: ProductManifest, available: Iterable[BlockManifest], kernel_provides: Iterable[str] = ()
) -> list[BlockManifest]:
    """Return the product's blocks in load order (providers before consumers).

    Checks: every listed block exists at that major version; every required capability has exactly one provider
    among the listed blocks (or the kernel); there is no dependency cycle.
    """
    by_id = {m.id: m for m in available}
    wanted = product.block_refs()

    chosen: dict[str, BlockManifest] = {}
    for block_id, major in wanted.items():
        manifest = by_id.get(block_id)
        if manifest is None:
            raise ResolutionError(f"{block_id} is not in the block library")
        if manifest.major != major:
            raise ResolutionError(f"{block_id}@{major} requested, but the library has major version {manifest.major}")
        if manifest.status == "retired":
            raise ResolutionError(f"{block_id} is retired and cannot be installed")
        chosen[block_id] = manifest

    providers: dict[str, list[str]] = {}
    for manifest in chosen.values():
        for cap in manifest.provides:
            providers.setdefault(cap, []).append(manifest.id)
    kernel = set(kernel_provides)

    deps: dict[str, set[str]] = {block_id: set() for block_id in chosen}
    for manifest in chosen.values():
        for cap in manifest.requires:
            if cap in kernel:
                continue
            found = providers.get(cap, [])
            if not found:
                raise ResolutionError(f"{manifest.id} requires {cap}, but no listed block provides it")
            if len(found) > 1:
                raise ResolutionError(
                    f"{cap} is provided by more than one block ({', '.join(sorted(found))}); choose one"
                )
            if found[0] != manifest.id:
                deps[manifest.id].add(found[0])

    order: list[str] = []
    state: dict[str, int] = {}  # 1 = visiting, 2 = done

    def visit(block_id: str, trail: tuple[str, ...]) -> None:
        if state.get(block_id) == 2:
            return
        if state.get(block_id) == 1:
            cycle = " -> ".join([*trail[trail.index(block_id) :], block_id])
            raise ResolutionError(f"dependency cycle: {cycle}")
        state[block_id] = 1
        for dep in sorted(deps[block_id]):
            visit(dep, (*trail, block_id))
        state[block_id] = 2
        order.append(block_id)

    for block_id in sorted(chosen):
        visit(block_id, ())
    return [chosen[b] for b in order]
