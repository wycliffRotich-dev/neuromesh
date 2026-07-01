import pytest

from app.domain.value_objects.resource_requirements import ResourceRequirements


def test_valid_resource_requirements() -> None:
    requirements = ResourceRequirements(
        cpu_cores=8,
        memory_mib=32768,
        vram_mib=24576,
    )

    assert requirements.cpu_cores == 8
    assert requirements.memory_mib == 32768
    assert requirements.vram_mib == 24576


def test_cpu_must_be_positive() -> None:
    with pytest.raises(ValueError):
        ResourceRequirements(
            cpu_cores=0,
            memory_mib=1024,
        )


def test_memory_must_be_positive() -> None:
    with pytest.raises(ValueError):
        ResourceRequirements(
            cpu_cores=1,
            memory_mib=0,
        )


def test_vram_cannot_be_negative() -> None:
    with pytest.raises(ValueError):
        ResourceRequirements(
            cpu_cores=1,
            memory_mib=1024,
            vram_mib=-1,
        )