# -*- coding: utf-8 -*-
"""Interface to collections simulated in V-REP.

Interface to collections simulated in V-REP provides an interface to a
collection of scene objects simulated in V-REP.
"""

import vrep

from vrepsim.base import Communicator
from vrepsim.constants import EMPTY_NAME
from vrepsim.exceptions import ConnectionError, ServerError


class Collection(Communicator):
    """Interface to a collection of scene objects simulated in V-REP."""

    def __init__(self, name, vrep_sim=None):
        super(Collection, self).__init__(vrep_sim)
        self._name = name
        self._handle = self._get_handle()

    @property
    def handle(self):
        """Collection handle."""
        return self._handle

    @property
    def name(self):
        """Collection name."""
        return self._name

    def get_names(self):
        """Retrieve names of component scene objects."""
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not retrieve names of {}: not connected to V-REP "
                "remote API server.".format(self._name))
        res, _, _, _, names = vrep.simxGetObjectGroupData(
            client_id, self._handle, 0, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not retrieve names of {}.".format(self._name))
        return names

    def get_orientations(self, prec=None):
        """Retrieve orientations of component scene objects, specified as Euler
        angles about x, y, and z axes of the absolute reference frame, each
        angle between -pi and pi.
        """
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not retrieve orientations of {}: not connected to "
                "V-REP remote API server.".format(self._name))
        res, _, _, orientations, _ = vrep.simxGetObjectGroupData(
            client_id, self._handle, 5, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not retrieve orientations of {}.".format(self._name))
        if prec is not None:
            orientations = [round(angle, prec) for angle in orientations]
        return [orientations[o:o+3] for o in range(0, len(orientations), 3)]

    def get_positions(self, prec=None):
        """Retrieve positions of component scene objects."""
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not retrieve positions of {}: not connected to V-REP "
                "remote API server.".format(self._name))
        res, _, _, positions, _ = vrep.simxGetObjectGroupData(
            client_id, self._handle, 3, vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not retrieve positions of {}.".format(self._name))
        if prec is not None:
            positions = [round(coord, prec) for coord in positions]
        return [positions[p:p+3] for p in range(0, len(positions), 3)]

    def _get_handle(self):
        """Retrieve collection handle."""
        if not self._name:
            raise RuntimeError("Could not retrieve handle to {}: missing name."
                               "".format(EMPTY_NAME))
        client_id = self.client_id
        if client_id is None:
            raise ConnectionError(
                "Could not retrieve handle to {}: not connected to V-REP "
                "remote API server.".format(self._name))
        res, handle = vrep.simxGetCollectionHandle(client_id, self._name,
                                                   vrep.simx_opmode_blocking)
        if res != vrep.simx_return_ok:
            raise ServerError(
                "Could not retrieve handle to {}.".format(self._name))
        return handle
