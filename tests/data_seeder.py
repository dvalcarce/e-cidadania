#/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2012 Cidadania S. Coop. Galega
#
# This file is part of e-cidadania.
#
# e-cidadania is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# e-cidadania is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with e-cidadania. If not, see <http://www.gnu.org/licenses/>.

from mockups import Mockup
from mockups.helpers import register

from django.contrib.auth.models import User
from django.db import models


class Error(Exception):
    """Base class for all exceptions raised by the seeder.
    """
    pass


class InvalidModelError(Error):
    """Raised when a model is not a valid Django model.
    """
    pass


class DataSeeder(object):
    """Class which contains the methods to seed data or fixtures for testing.
    
    We presently wrap our methods around Mockup. 
    """
    
    def __init__(self):
        #Register User with Mockup
        register(User, Mockup)
    
    def seed(self, model, constraints=None, follow_fk=None, generate_fk=None,
             follow_m2m=None, factory=None, model_properties=None, commit=True):
        """Creates and saves an instance of 'model' in the database.
        
        The values generated by Mockup class for the fields may not be 
        acceptable. Custom values for the fields can be provided in 
        model_properties.
        
        Parameters:
            ``model``: A model class which is used to create the test data.

            ``constraints``: A list of callables. The constraints are used to
            verify if the created model instance may be used. The callable
            gets the actual model as first and the instance as second
            parameter. The instance is not populated yet at this moment.  The
            callable may raise an :exc:`InvalidConstraint` exception to
            indicate which fields violate the constraint.

            ``follow_fk``: A boolean value indicating if foreign keys should be
            set to random, already existing, instances of the related model.

            ``generate_fk``: A boolean which indicates if related models should
            also be created with random values. The *follow_fk* parameter will
            be ignored if *generate_fk* is set to ``True``.

            ``follow_m2m``: A tuple containing minium and maximum of model
            instances that are assigned to ``ManyToManyField``. No new
            instances will be created. Default is (1, 5).  You can ignore
            ``ManyToManyField`` fields by setting this parameter to ``False``.

            ``generate_m2m``: A tuple containing minimum and maximum number of
            model instance that are newly created and assigned to the
            ``ManyToManyField``. Default is ``False`` which disables the
            generation of new related instances. The value of ``follow_m2m``
            will be ignored if this parameter is set.

            ``factory``: A Factory *instance*, overriding the one defined in the
            Mockup class.
            
            ``model_properties``: A dict containing the custom properties 
            for the ``model``
            
            ``commit``: A boolean which is set to True by default and indicates
            whether the model should be saved to the database or not.
                     
        """
        
        #if not isinstance(model, models.Model):
        #    raise InvalidModelError("%s is not a valid Django model." % model)
        if model_properties is None:
            model_properties = {}
        
        # Creates and randomly populates the data
        mockup = Mockup(model, constraints=constraints, follow_fk=follow_fk,
                        generate_fk=generate_fk, follow_m2m=follow_m2m, 
                        factory=factory)
        created_model = mockup.create_one(commit=commit)
        
        # set the attributes of the model as provided in model_properties
        for key in model_properties.iterkeys():
            setattr(created_model, key, model_properties[key])
        if commit:
            created_model.save()
        return created_model

    def seedn(self, count, model, constraints=None, follow_fk=None, 
              generate_fk=None, follow_m2m=None, factory=None,
              model_properties=None, commit=True ):
        """Creates and saves n instances of 'model' in the database and returns
        a list of all those saved instances.
        
        The method uses self.seed to generate a list of instances of ``model``
        ``count`` number of times.
        """

        obj_list = []
        for _ in xrange(count):
            obj = self.seed(model=model, constraints=constraints, 
                            follow_fk=follow_fk, generate_fk=generate_fk,
                            follow_m2m=follow_m2m, factory=factory,
                            model_properties=model_properties, commit=commit)
            obj_list.append(obj)
        
        return obj_list
        
seeder = DataSeeder()       