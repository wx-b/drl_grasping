from gym.envs.registration import register

from .reach import Reach, ReachColorImage, ReachDepthImage, ReachOctree
from .grasp import Grasp, GraspOctree

# Reach
REACH_MAX_EPISODE_STEPS: int = 100
REACH_AGENT_RATE: float = 2.5
REACH_PHYSICS_RATE: float = 100.0
REACH_RTF: float = 15.0
register(
    id='Reach-Gazebo-v0',
    entry_point='gym_ignition.runtimes.gazebo_runtime:GazeboRuntime',
    max_episode_steps=REACH_MAX_EPISODE_STEPS,
    kwargs={'task_cls': Reach,
            'agent_rate': REACH_AGENT_RATE,
            'physics_rate': REACH_PHYSICS_RATE,
            'real_time_factor': REACH_RTF,
            'restrict_position_goal_to_workspace': True,
            'sparse_reward': False,
            'act_quick_reward': -0.01,
            'required_accuracy': 0.05,
            'verbose': False,
            })
register(
    id='Reach-ColorImage-Gazebo-v0',
    entry_point='gym_ignition.runtimes.gazebo_runtime:GazeboRuntime',
    max_episode_steps=REACH_MAX_EPISODE_STEPS,
    kwargs={'task_cls': ReachColorImage,
            'agent_rate': REACH_AGENT_RATE,
            'physics_rate': REACH_PHYSICS_RATE,
            'real_time_factor': REACH_RTF,
            'restrict_position_goal_to_workspace': True,
            'sparse_reward': False,
            'act_quick_reward': -0.01,
            'required_accuracy': 0.05,
            'verbose': False,
            })
register(
    id='Reach-DepthImage-Gazebo-v0',
    entry_point='gym_ignition.runtimes.gazebo_runtime:GazeboRuntime',
    max_episode_steps=REACH_MAX_EPISODE_STEPS,
    kwargs={'task_cls': ReachDepthImage,
            'agent_rate': REACH_AGENT_RATE,
            'physics_rate': REACH_PHYSICS_RATE,
            'real_time_factor': REACH_RTF,
            'restrict_position_goal_to_workspace': True,
            'sparse_reward': False,
            'act_quick_reward': -0.01,
            'required_accuracy': 0.05,
            'verbose': False,
            })
register(
    id='Reach-Octree-Gazebo-v0',
    entry_point='gym_ignition.runtimes.gazebo_runtime:GazeboRuntime',
    max_episode_steps=REACH_MAX_EPISODE_STEPS,
    kwargs={'task_cls': ReachOctree,
            'agent_rate': REACH_AGENT_RATE,
            'physics_rate': REACH_PHYSICS_RATE,
            'real_time_factor': REACH_RTF,
            'restrict_position_goal_to_workspace': True,
            'sparse_reward': False,
            'act_quick_reward': -0.01,
            'required_accuracy': 0.05,
            'octree_depth': 5,
            'octree_full_depth': 2,
            'octree_include_color': False,
            'octree_n_stacked': 2,
            'octree_max_size': 20000,
            'verbose': False,
            })
register(
    id='Reach-OctreeWithColor-Gazebo-v0',
    entry_point='gym_ignition.runtimes.gazebo_runtime:GazeboRuntime',
    max_episode_steps=REACH_MAX_EPISODE_STEPS,
    kwargs={'task_cls': ReachOctree,
            'agent_rate': REACH_AGENT_RATE,
            'physics_rate': REACH_PHYSICS_RATE,
            'real_time_factor': REACH_RTF,
            'restrict_position_goal_to_workspace': True,
            'sparse_reward': False,
            'act_quick_reward': -0.01,
            'required_accuracy': 0.05,
            'octree_depth': 5,
            'octree_full_depth': 2,
            'octree_include_color': True,
            'octree_n_stacked': 2,
            'octree_max_size': 25000,
            'verbose': False,
            })

# Grasp
GRASP_MAX_EPISODE_STEPS: int = 250
GRASP_AGENT_RATE: float = 2.5
GRASP_PHYSICS_RATE: float = 200.0
GRASP_RTF: float = 10.0
register(
    id='Grasp-Octree-Gazebo-v0',
    entry_point='gym_ignition.runtimes.gazebo_runtime:GazeboRuntime',
    max_episode_steps=GRASP_MAX_EPISODE_STEPS,
    kwargs={'task_cls': GraspOctree,
            'agent_rate': GRASP_AGENT_RATE,
            'physics_rate': GRASP_PHYSICS_RATE,
            'real_time_factor': GRASP_RTF,
            'restrict_position_goal_to_workspace': True,
            'gripper_dead_zone': 0.25,
            'full_3d_orientation': False,
            'sparse_reward': False,
            'required_reach_distance': 0.1,
            'required_lift_height': 0.25,
            'act_quick_reward': -0.001,
            'curriculum_enable_stages': True,
            'curriculum_enable_workspace_scale': True,
            'curriculum_success_rate_threshold': 0.5,
            'curriculum_success_rate_rolling_average_n': 20,
            'curriculum_restart_every_n_steps': 0,
            'curriculum_min_workspace_scale': 0.4,
            'curriculum_stage_reward_multiplier': 0.5,
            'curriculum_stage_increase_rewards': False,
            'curriculum_scale_negative_reward': False,
            'curriculum_n_ground_collisions_till_termination': 15,
            'curriculum_reward_multiplier': 1.0,
            'curriculum_reach_dense_reward_multiplier': 2.0,
            'curriculum_lift_dense_reward_multiplier': 10.0,
            'curriculum_skip_grasp_stage': True,
            'curriculum_restart_exploration_at_start': True,
            'octree_depth': 5,
            'octree_full_depth': 2,
            'octree_include_color': False,
            'octree_n_stacked': 2,
            'octree_max_size': 30000,
            'verbose': False,
            })
register(
    id='Grasp-OctreeWithColor-Gazebo-v0',
    entry_point='gym_ignition.runtimes.gazebo_runtime:GazeboRuntime',
    max_episode_steps=GRASP_MAX_EPISODE_STEPS,
    kwargs={'task_cls': GraspOctree,
            'agent_rate': GRASP_AGENT_RATE,
            'physics_rate': GRASP_PHYSICS_RATE,
            'real_time_factor': GRASP_RTF,
            'restrict_position_goal_to_workspace': True,
            'gripper_dead_zone': 0.25,
            'full_3d_orientation': False,
            'sparse_reward': False,
            'required_reach_distance': 0.1,
            'required_lift_height': 0.25,
            'act_quick_reward': 0.0,
            # If disabled, curriculum skips directly to the last stage
            'curriculum_enable_stages': True,
            'curriculum_enable_workspace_scale': True,
            'curriculum_success_rate_threshold': 0.5,
            'curriculum_success_rate_rolling_average_n': 20,
            'curriculum_restart_every_n_steps': 0,
            'curriculum_min_workspace_scale': 0.4,
            'curriculum_stage_reward_multiplier': 2.0,
            'curriculum_stage_increase_rewards': True,
            'curriculum_scale_negative_reward': False,
            'curriculum_n_ground_collisions_till_termination': 15,
            'curriculum_reward_multiplier': 1.0,
            'curriculum_reach_dense_reward_multiplier': 2.0,
            'curriculum_lift_dense_reward_multiplier': 10.0,
            'curriculum_skip_grasp_stage': True,
            # Flag useful when continuing with training of pre-trained agent and ent_coef optimizer is not loaded properly
            'curriculum_restart_exploration_at_start': False,
            'octree_depth': 5,
            'octree_full_depth': 2,
            'octree_include_color': True,
            'octree_n_stacked': 2,
            'octree_max_size': 100000,
            'verbose': False,
            })
