# global
import ivy
from ivy.func_wrapper import with_supported_dtypes
from ivy.functional.frontends.paddle.func_wrapper import (
    to_ivy_arrays_and_back,
)
from ivy.functional.ivy.experimental.manipulation import _to_tf_padding


@with_supported_dtypes(
    {"2.5.1 and below": ("complex64", "complex128")},
    "paddle",
)
@to_ivy_arrays_and_back
def fft(x, n=None, axis=-1.0, norm="backward", name=None):
    ret = ivy.fft(ivy.astype(x, "complex128"), axis, norm=norm, n=n)
    return ivy.astype(ret, x.dtype)


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "int32",
            "int64",
            "float32",
            "float64",
            "complex64",
            "complex128",
        )
    },
    "paddle",
)
@to_ivy_arrays_and_back
def fftshift(x, axes=None, name=None):
    shape = x.shape

    if axes is None:
        axes = tuple(range(x.ndim))
        shifts = [(dim // 2) for dim in shape]
    elif isinstance(axes, int):
        shifts = shape[axes] // 2
    else:
        shifts = ivy.concat([shape[ax] // 2 for ax in axes])

    roll = ivy.roll(x, shifts, axis=axes)

    return roll


@with_supported_dtypes(
    {"2.5.1 and below": ("complex64", "complex128")},
    "paddle",
)
@to_ivy_arrays_and_back
def hfft(x, n=None, axis=-1, norm="backward", name=None):
    """Compute the FFT of a signal that has Hermitian symmetry, resulting in a real
    spectrum."""
    # Determine the input shape and axis length
    input_shape = x.shape
    input_len = input_shape[axis]

    # Calculate n if not provided
    if n is None:
        n = 2 * (input_len - 1)

    # Perform the FFT along the specified axis
    result = ivy.fft(x, axis, n=n, norm=norm)

    return ivy.real(result)


@with_supported_dtypes(
    {"2.5.1 and below": ("complex64", "complex128")},
    "paddle",
)
@to_ivy_arrays_and_back
def ifft(x, n=None, axis=-1.0, norm="backward", name=None):
    ret = ivy.ifft(ivy.astype(x, "complex128"), axis, norm=norm, n=n)
    return ivy.astype(ret, x.dtype)


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "int32",
            "int64",
            "float32",
            "float64",
        )
    },
    "paddle",
)
@to_ivy_arrays_and_back
def ifftshift(x, axes=None, name=None):
    shape = x.shape

    if axes is None:
        axes = tuple(range(x.ndim))
        shifts = [-(dim // 2) for dim in shape]
    elif isinstance(axes, int):
        shifts = -(shape[axes] // 2)
    else:
        shifts = ivy.concat([-shape[ax] // 2 for ax in axes])

    roll = ivy.roll(x, shifts, axis=axes)

    return roll


@with_supported_dtypes(
    {"2.5.1 and below": ("complex64", "complex128")},
    "paddle",
)
@to_ivy_arrays_and_back
def irfft(x, n=None, axis=-1.0, norm="backward", name=None):
    if n is None:
        n = 2 * (x.shape[axis] - 1)

    pos_freq_terms = ivy.take_along_axis(x, range(n // 2 + 1), axis)
    neg_freq_terms = ivy.conj(pos_freq_terms[1:-1][::-1])
    combined_freq_terms = ivy.concat((pos_freq_terms, neg_freq_terms), axis=axis)
    time_domain = ivy.ifft(combined_freq_terms, axis, norm=norm, n=n)
    if ivy.isreal(x):
        time_domain = ivy.real(time_domain)
    return time_domain


@with_supported_dtypes(
    {"2.5.1 and below": ("complex64", "complex128")},
    "paddle",
)
@to_ivy_arrays_and_back
def irfftn(x, s=None, axes=None, norm="backward", name=None):
    x = ivy.array(x)
    if ivy.is_complex_dtype(x.dtype):
        output_dtype = 'float32' if x.dtype == 'complex64' else 'float64'
    else:
        output_dtype = 'float32'  # default

    time_domain = None  # Initialize with a default value

    if axes is None:
        axes = list(range(len(x.shape)))
    if s is None:
        s = [2 * x.shape[axis] - 2 for axis in axes]

    if len(axes) == 1:
        pos_freq_terms = x[..., :s[0]//2+1]
        neg_freq_terms = ivy.conj(pos_freq_terms[..., 1:-1][..., ::-1])
        combined_freq_terms = ivy.concat((pos_freq_terms, neg_freq_terms), axis=axes[0])
        complex_result = ivy.ifft(combined_freq_terms, dim=axes[0], norm=norm, n=s[0])
        real_result = ivy.real(complex_result)
        result_t=ivy.astype(real_result, output_dtype)
        return result_t  

    # Multi-dimensional inverse FFT
    """
    if s is None:
        n = [x.shape[axis] * 2 - 2 for axis in axes]
    else:
        n = [s_i * 2 - 2 for s_i in s]
        
    # Prepare the combined frequency term
    # pos_freq_terms = ...  # Actual code to prepare positive frequency terms
    # neg_freq_terms = ...  # Actual code to prepare negative frequency terms
    # combined_freq_terms = ...  # Actual code to combine frequency terms
    
    # Apply multi-dimensional inverse FFT
    time_domain = ivy.ifftn(combined_freq_terms, axes=axes, norm=norm, shape=n)
    
    # Check if the input was real and return only the real part if so
    if ivy.isreal(x):
        time_domain = ivy.real(time_domain)
    """
    # Return the inverse FFT
    return time_domain