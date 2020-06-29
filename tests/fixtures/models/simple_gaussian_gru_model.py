"""Simple GaussianGRUModel for testing."""
import tensorflow as tf

from garage.tf.distributions import DiagonalGaussian
from garage.tf.models import Model


class SimpleGaussianGRUModel(Model):
    """Simple GaussianGRUModel for testing.

    Args:
        output_dim (int): Dimension of the network output.
        hidden_dim (int): Hidden dimension for GRU cell.
        name (str): Model name, also the variable scope.
        args (list): Unused positionl arguments.
        kwargs (dict): Unused keyword arguments.

    """

    # pylint: disable=arguments-differ
    def __init__(self,
                 output_dim,
                 hidden_dim,
                 *args,
                 name='SimpleGaussianGRUModel',
                 **kwargs):
        del args
        del kwargs
        super().__init__(name)
        self.output_dim = output_dim
        self.hidden_dim = hidden_dim

    def network_input_spec(self):
        """Network input spec.

        Return:
            list[str]: List of key(str) for the network outputs.

        """
        return ['full_input', 'step_input', 'step_hidden_input']

    def network_output_spec(self):
        """Network output spec.

        Return:
            list[str]: List of key(str) for the network outputs.

        """
        return [
            'mean', 'step_mean', 'log_std', 'step_log_std', 'step_hidden',
            'init_hidden', 'dist'
        ]

    def _build(self, obs_input, step_obs_input, step_hidden, name=None):
        """Build model given input placeholder(s).

        Args:
            obs_input (tf.Tensor): Place holder for entire time-series
                inputs.
            step_obs_input (tf.Tensor): Place holder for step inputs.
            step_hidden (tf.Tensor): Place holder for step hidden state.
            name (str): Inner model name, also the variable scope of the
                inner model, if exist. One example is
                garage.tf.models.Sequential.

        Return:
            tf.Tensor: Entire time-series means.
            tf.Tensor: Step mean.
            tf.Tensor: Entire time-series log std.
            tf.Tensor: Step log std.
            tf.Tensor: Step hidden state.
            tf.Tensor: Initial hidden state.
            garage.distributions.DiagonalGaussian: Distribution.

        """
        del name
        return_var = tf.compat.v1.get_variable(
            'return_var', (), initializer=tf.constant_initializer(0.5))
        mean = log_std = tf.fill(
            (tf.shape(obs_input)[0], tf.shape(obs_input)[1], self.output_dim),
            return_var)
        step_mean = step_log_std = tf.fill(
            (tf.shape(step_obs_input)[0], self.output_dim), return_var)

        hidden_init_var = tf.compat.v1.get_variable(
            name='initial_hidden',
            shape=(self.hidden_dim, ),
            initializer=tf.zeros_initializer(),
            trainable=False,
            dtype=tf.float32)

        dist = DiagonalGaussian(self.output_dim)

        return (mean, step_mean, log_std, step_log_std, step_hidden,
                hidden_init_var, dist)
