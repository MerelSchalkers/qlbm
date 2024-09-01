from qiskit_aer import AerSimulator

from qlbm.components import (
    CQLBM,
    EmptyPrimitive,
    GridMeasurement,
)
from qlbm.components.collisionless import CollisionlessInitialConditions3DSlim
from qlbm.infra import QiskitRunner, SimulationConfig
from qlbm.lattice import CollisionlessLattice
from qlbm.tools.utils import create_directory_and_parents

if __name__ == "__main__":
    # Example with mixed boundary conditions
    # lattice_file = "demos/lattices/2d_16x16_2_obstacle_mixed.json"
    lattice_file = "demos/lattices/3d_8x8x8_1_obstacle.json"
    lattice = CollisionlessLattice(lattice_file)

    lattice_name = lattice_file.split("/")[-1].split(".")[0].replace("_", "-")
    output_dir = f"qlbm-output/3d-impl-test-{lattice_name}-qiskit"

    create_directory_and_parents(output_dir)

    cfg = SimulationConfig(
        initial_conditions=CollisionlessInitialConditions3DSlim(lattice),
        algorithm=CQLBM(lattice),
        postprocessing=EmptyPrimitive(lattice),
        measurement=GridMeasurement(lattice),
        target_platform="QISKIT",
        compiler_platform="QISKIT",
        optimization_level=0,
        statevector_sampling=True,
        execution_backend=AerSimulator(method="statevector"),
        sampling_backend=AerSimulator(method="statevector"),
    )
    cfg.prepare_for_simulation()

    # Create a runner object to simulate the circuit
    runner = QiskitRunner(
        cfg,
        lattice,
    )

    print(lattice.num_total_qubits)

    # Number of shots to simulate for each timestep when running the circuit
    num_shots = 2**11
    # Number of shots to simulate
    num_steps = 5

    # Simulate the circuits using both snapshots and sampling
    runner.run(
        num_steps,  # Number of time steps
        num_shots,  # Number of shots per time step
        output_dir,
        statevector_snapshots=True,
    )
