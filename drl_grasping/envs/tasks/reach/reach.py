from drl_grasping.envs.tasks.manipulation import Manipulation
from gym_ignition.utils.typing import Action, Reward, Observation
from gym_ignition.utils.typing import ActionSpace, ObservationSpace
from typing import Tuple
import abc
import gym
import numpy as np


class Reach(Manipulation, abc.ABC):

    # Overwrite parameters for ManipulationGazeboEnvRandomizer
    _robot_initial_joint_positions: Tuple[float, ...] = (0.0,
                                                         0.0,
                                                         0.0,
                                                         -1.57,
                                                         0.0,
                                                         1.57,
                                                         0.79,
                                                         0.0,
                                                         0.0)
    _object_enable: bool = True
    _workspace_centre:  Tuple[float, float, float] = (0.5, 0, 0.25)
    _workspace_volume: Tuple[float, float, float] = (0.6, 0.6, 0.6)
    _object_spawn_volume: Tuple[float, float, float] = (0.3, 0.3, 0.3)
    _object_spawn_height: float = 0.0
    _object_collision: bool = False
    _object_static: bool = True
    _object_color: Tuple[float, float, float, float] = (0.0, 0.0, 1.0, 1.0)

    def __init__(self,
                 agent_rate: float,
                 restrict_position_goal_to_workspace: bool = True,
                 shaped_reward: bool = True,
                 act_quick_reward: float = 0.0,
                 required_accuracy: float = 0.05,
                 verbose: bool = True,
                 **kwargs):

        # Initialize the Task base class
        Manipulation.__init__(self,
                              agent_rate=agent_rate,
                              restrict_position_goal_to_workspace=restrict_position_goal_to_workspace,
                              verbose=verbose,
                              **kwargs)

        # Additional parameters
        self._shaped_reward: bool = shaped_reward
        self._act_quick_reward: float = act_quick_reward
        self._required_accuracy: float = required_accuracy

        # Flag indicating if the task is done (performance - get_reward + is_done)
        self._is_done: bool = False

        # Distance to target in the previous step (or after reset)
        self._previous_distance: float = None

    def create_action_space(self) -> ActionSpace:

        # 0:3 - (x, y, z) displacement
        #     - rescaled to metric units before use
        return gym.spaces.Box(low=-1.0,
                              high=1.0,
                              shape=(3,),
                              dtype=np.float32)

    def create_observation_space(self) -> ObservationSpace:

        # 0:3 - (x, y, z) end effector position
        # 3:6 - (x, y, z) target position
        # Note: These could theoretically be restricted to the workspace and object spawn area instead of inf
        return gym.spaces.Box(low=-np.inf,
                              high=np.inf,
                              shape=(6,),
                              dtype=np.float32)

    def set_action(self, action: Action):

        if self._verbose:
            print(f"action: {action}")

        # Set position goal
        relative_position = action[0:3]
        self.set_position_goal(relative=relative_position)

        # Set orientation goal
        absolute_quat_xyzw = (1.0, 0.0, 0.0, 0.0)
        self.set_orientation_goal(absolute=absolute_quat_xyzw)

        # Plan and execute motion to target pose
        self.moveit2.plan_kinematic_path(allowed_planning_time=0.1)
        self.moveit2.execute()

    def get_observation(self) -> Observation:

        # Get current end-effector and target positions
        ee_position = self.get_ee_position()
        target_position = self.get_target_position()

        # Create the observation
        observation = Observation(np.concatenate([ee_position,
                                                  target_position]))

        if self._verbose:
            print(f"\nobservation: {observation}")

        # Return the observation
        return observation

    def get_reward(self) -> Reward:

        reward = 0.0

        # Compute the current distance to the target
        current_distance = self.get_distance_to_target()

        # Return reward of 1.0 if target is reached and mark the episode done
        if current_distance < self._required_accuracy:
            reward += 1.0
            self._is_done = True

        # If the episode is not done, give a shaped/act-quick reward (if enabled)
        if not self._is_done:
            if self._shaped_reward:
                # Give reward based on how much closer robot got relative to the target
                reward += self._previous_distance - current_distance
                self._previous_distance = current_distance

            # Subtract a small reward each step to provide incentive to act quickly (if enabled)
            if self._act_quick_reward < 0.0:
                reward += self._act_quick_reward

        if self._verbose:
            print(f"reward: {reward}")

        return Reward(reward)

    def is_done(self) -> bool:

        done = self._is_done

        if self._verbose:
            print(f"done: {done}")

        return done

    def reset_task(self):

        if self._verbose:
            print(f"\nreset task")

        self._is_done = False

        if self._shaped_reward:
            # Compute and store the original distance if rewards should be normalized
            self._previous_distance = self.get_distance_to_target()

    def get_distance_to_target(self) -> Tuple[float, float, float]:

        # Get current end-effector and target positions
        ee_position = self.get_ee_position()
        target_position = self.get_target_position()

        # Compute the current distance to the target
        return np.linalg.norm([ee_position[0] - target_position[0],
                               ee_position[1] - target_position[1],
                               ee_position[2] - target_position[2]])

    def get_target_position(self) -> Tuple[float, float, float]:

        target_object = self.world.get_model(self.object_names[0]).to_gazebo()
        return target_object.get_link(link_name=target_object.link_names()[0]).position()