"""Tests for backend module """

# Author: Remi Flamary <remi.flamary@polytechnique.edu>
#         Nicolas Courty <ncourty@irisa.fr>
#
# License: MIT License

import ot
import ot.backend
from ot.backend import torch, jax

import pytest

import numpy as np
from numpy.testing import assert_array_almost_equal_nulp

from ot.backend import get_backend, get_backend_list, to_numpy


def test_get_backend_list():

    lst = get_backend_list()

    assert len(lst) > 0
    assert isinstance(lst[0], ot.backend.NumpyBackend)


def test_to_numpy(nx):

    v = nx.zeros(10)
    M = nx.ones((10, 10))

    v2 = to_numpy(v)
    assert isinstance(v2, np.ndarray)

    v2, M2 = to_numpy(v, M)
    assert isinstance(M2, np.ndarray)


def test_get_backend():

    A = np.zeros((3, 2))
    B = np.zeros((3, 1))

    nx = get_backend(A)
    assert nx.__name__ == 'numpy'

    nx = get_backend(A, B)
    assert nx.__name__ == 'numpy'

    # error if no parameters
    with pytest.raises(ValueError):
        get_backend()

    # error if unknown types
    with pytest.raises(ValueError):
        get_backend(1, 2.0)

    # test torch
    if torch:

        A2 = torch.from_numpy(A)
        B2 = torch.from_numpy(B)

        nx = get_backend(A2)
        assert nx.__name__ == 'torch'

        nx = get_backend(A2, B2)
        assert nx.__name__ == 'torch'

        # test not unique types in input
        with pytest.raises(ValueError):
            get_backend(A, B2)

    if jax:

        A2 = jax.numpy.array(A)
        B2 = jax.numpy.array(B)

        nx = get_backend(A2)
        assert nx.__name__ == 'jax'

        nx = get_backend(A2, B2)
        assert nx.__name__ == 'jax'

        # test not unique types in input
        with pytest.raises(ValueError):
            get_backend(A, B2)


def test_convert_between_backends(nx):

    A = np.zeros((3, 2))
    B = np.zeros((3, 1))

    A2 = nx.from_numpy(A)
    B2 = nx.from_numpy(B)

    assert isinstance(A2, nx.__type__)
    assert isinstance(B2, nx.__type__)

    nx2 = get_backend(A2, B2)

    assert nx2.__name__ == nx.__name__

    assert_array_almost_equal_nulp(nx.to_numpy(A2), A)
    assert_array_almost_equal_nulp(nx.to_numpy(B2), B)


def test_empty_backend():

    rnd = np.random.RandomState(0)
    M = rnd.randn(10, 3)
    v = rnd.randn(3)

    nx = ot.backend.Backend()

    with pytest.raises(NotImplementedError):
        nx.from_numpy(M)
    with pytest.raises(NotImplementedError):
        nx.to_numpy(M)
    with pytest.raises(NotImplementedError):
        nx.set_gradients(0, 0, 0)
    with pytest.raises(NotImplementedError):
        nx.zeros((10, 3))
    with pytest.raises(NotImplementedError):
        nx.ones((10, 3))
    with pytest.raises(NotImplementedError):
        nx.arange(10, 1, 2)
    with pytest.raises(NotImplementedError):
        nx.full((10, 3), 3.14)
    with pytest.raises(NotImplementedError):
        nx.eye((10, 3))
    with pytest.raises(NotImplementedError):
        nx.sum(M)
    with pytest.raises(NotImplementedError):
        nx.cumsum(M)
    with pytest.raises(NotImplementedError):
        nx.max(M)
    with pytest.raises(NotImplementedError):
        nx.min(M)
    with pytest.raises(NotImplementedError):
        nx.maximum(v, v)
    with pytest.raises(NotImplementedError):
        nx.minimum(v, v)
    with pytest.raises(NotImplementedError):
        nx.abs(M)
    with pytest.raises(NotImplementedError):
        nx.log(M)
    with pytest.raises(NotImplementedError):
        nx.exp(M)
    with pytest.raises(NotImplementedError):
        nx.sqrt(M)
    with pytest.raises(NotImplementedError):
        nx.power(v, 2)
    with pytest.raises(NotImplementedError):
        nx.dot(v, v)
    with pytest.raises(NotImplementedError):
        nx.norm(M)
    with pytest.raises(NotImplementedError):
        nx.exp(M)
    with pytest.raises(NotImplementedError):
        nx.any(M)
    with pytest.raises(NotImplementedError):
        nx.isnan(M)
    with pytest.raises(NotImplementedError):
        nx.isinf(M)
    with pytest.raises(NotImplementedError):
        nx.einsum('ij->i', M)
    with pytest.raises(NotImplementedError):
        nx.sort(M)
    with pytest.raises(NotImplementedError):
        nx.argsort(M)
    with pytest.raises(NotImplementedError):
        nx.searchsorted(v, v)
    with pytest.raises(NotImplementedError):
        nx.flip(M)
    with pytest.raises(NotImplementedError):
        nx.outer(v, v)
    with pytest.raises(NotImplementedError):
        nx.clip(M, -1, 1)
    with pytest.raises(NotImplementedError):
        nx.repeat(M, 0, 1)
    with pytest.raises(NotImplementedError):
        nx.take_along_axis(M, v, 0)
    with pytest.raises(NotImplementedError):
        nx.concatenate([v, v])
    with pytest.raises(NotImplementedError):
        nx.zero_pad(M, v)
    with pytest.raises(NotImplementedError):
        nx.argmax(M)
    with pytest.raises(NotImplementedError):
        nx.mean(M)
    with pytest.raises(NotImplementedError):
        nx.std(M)
    with pytest.raises(NotImplementedError):
        nx.linspace(0, 1, 50)
    with pytest.raises(NotImplementedError):
        nx.meshgrid(v, v)
    with pytest.raises(NotImplementedError):
        nx.diag(M)
    with pytest.raises(NotImplementedError):
        nx.unique([M, M])
    with pytest.raises(NotImplementedError):
        nx.logsumexp(M)
    with pytest.raises(NotImplementedError):
        nx.stack([M, M])
    with pytest.raises(NotImplementedError):
        nx.reshape(M, (5, 3, 2))


def test_func_backends(nx):

    rnd = np.random.RandomState(0)
    M = rnd.randn(10, 3)
    v = rnd.randn(3)
    val = np.array([1.0])

    lst_tot = []

    for nx in [ot.backend.NumpyBackend(), nx]:

        print('Backend: ', nx.__name__)

        lst_b = []
        lst_name = []

        Mb = nx.from_numpy(M)
        vb = nx.from_numpy(v)
        val = nx.from_numpy(val)

        A = nx.set_gradients(val, v, v)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('set_gradients')

        A = nx.zeros((10, 3))
        A = nx.zeros((10, 3), type_as=Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('zeros')

        A = nx.ones((10, 3))
        A = nx.ones((10, 3), type_as=Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('ones')

        A = nx.arange(10, 1, 2)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('arange')

        A = nx.full((10, 3), 3.14)
        A = nx.full((10, 3), 3.14, type_as=Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('full')

        A = nx.eye(10, 3)
        A = nx.eye(10, 3, type_as=Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('eye')

        A = nx.sum(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('sum')

        A = nx.sum(Mb, axis=1, keepdims=True)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('sum(axis)')

        A = nx.cumsum(Mb, 0)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('cumsum(axis)')

        A = nx.max(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('max')

        A = nx.max(Mb, axis=1, keepdims=True)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('max(axis)')

        A = nx.min(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('min')

        A = nx.min(Mb, axis=1, keepdims=True)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('min(axis)')

        A = nx.maximum(vb, 0)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('maximum')

        A = nx.minimum(vb, 0)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('minimum')

        A = nx.abs(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('abs')

        A = nx.log(A)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('log')

        A = nx.exp(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('exp')

        A = nx.sqrt(nx.abs(Mb))
        lst_b.append(nx.to_numpy(A))
        lst_name.append('sqrt')

        A = nx.power(Mb, 2)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('power')

        A = nx.dot(vb, vb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('dot(v,v)')

        A = nx.dot(Mb, vb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('dot(M,v)')

        A = nx.dot(Mb, Mb.T)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('dot(M,M)')

        A = nx.norm(vb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('norm')

        A = nx.any(vb > 0)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('any')

        A = nx.isnan(vb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('isnan')

        A = nx.isinf(vb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('isinf')

        A = nx.einsum('ij->i', Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('einsum(ij->i)')

        A = nx.einsum('ij,j->i', Mb, vb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('nx.einsum(ij,j->i)')

        A = nx.einsum('ij->i', Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('nx.einsum(ij->i)')

        A = nx.sort(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('sort')

        A = nx.argsort(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('argsort')

        A = nx.searchsorted(Mb, Mb, 'right')
        lst_b.append(nx.to_numpy(A))
        lst_name.append('searchsorted')

        A = nx.flip(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('flip')

        A = nx.outer(vb, vb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('outer')

        A = nx.clip(vb, 0, 1)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('clip')

        A = nx.repeat(Mb, 0)
        A = nx.repeat(Mb, 2, -1)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('repeat')

        A = nx.take_along_axis(vb, nx.arange(3), -1)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('take_along_axis')

        A = nx.concatenate((Mb, Mb), -1)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('concatenate')

        A = nx.zero_pad(Mb, len(Mb.shape) * [(3, 3)])
        lst_b.append(nx.to_numpy(A))
        lst_name.append('zero_pad')

        A = nx.argmax(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('argmax')

        A = nx.mean(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('mean')

        A = nx.std(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('std')

        A = nx.linspace(0, 1, 50)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('linspace')

        X, Y = nx.meshgrid(vb, vb)
        lst_b.append(np.stack([nx.to_numpy(X), nx.to_numpy(Y)]))
        lst_name.append('meshgrid')

        A = nx.diag(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('diag2D')

        A = nx.diag(vb, 1)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('diag1D')

        A = nx.unique(nx.from_numpy(np.stack([M, M])))
        lst_b.append(nx.to_numpy(A))
        lst_name.append('unique')

        A = nx.logsumexp(Mb)
        lst_b.append(nx.to_numpy(A))
        lst_name.append('logsumexp')

        A = nx.stack([Mb, Mb])
        lst_b.append(nx.to_numpy(A))
        lst_name.append('stack')

        A = nx.reshape(Mb, (5, 3, 2))
        lst_b.append(nx.to_numpy(A))
        lst_name.append('reshape')

        lst_tot.append(lst_b)

    lst_np = lst_tot[0]
    lst_b = lst_tot[1]

    for a1, a2, name in zip(lst_np, lst_b, lst_name):
        if not np.allclose(a1, a2):
            print('Assert fail on: ', name)
        assert np.allclose(a1, a2, atol=1e-7)


def test_gradients_backends():

    rnd = np.random.RandomState(0)
    v = rnd.randn(10)
    c = rnd.randn()
    e = rnd.randn()

    if torch:

        nx = ot.backend.TorchBackend()

        v2 = torch.tensor(v, requires_grad=True)
        c2 = torch.tensor(c, requires_grad=True)

        val = c2 * torch.sum(v2 * v2)

        val2 = nx.set_gradients(val, (v2, c2), (v2, c2))

        val2.backward()

        assert torch.equal(v2.grad, v2)
        assert torch.equal(c2.grad, c2)

    if jax:
        nx = ot.backend.JaxBackend()
        with jax.checking_leaks():
            def fun(a, b, d):
                val = b * nx.sum(a ** 4) + d
                return nx.set_gradients(val, (a, b, d), (a, b, 2 * d))
            grad_val = jax.grad(fun, argnums=(0, 1, 2))(v, c, e)

        np.testing.assert_almost_equal(fun(v, c, e), c * np.sum(v ** 4) + e, decimal=4)
        np.testing.assert_allclose(grad_val[0], v, atol=1e-4)
        np.testing.assert_allclose(grad_val[2], 2 * e, atol=1e-4)