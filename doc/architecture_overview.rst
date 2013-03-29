=====================
Architecture Overview
=====================
:Author: Chris Martel <chris@codeways.org>
:Date: 2013-03-29 11:23:51+01:00
:Description: A layout of the general architectural conventions for the system.

System layout
-------------
The system consists of three basic layers:

#. Controller/Views: handling user interaction along request/response flow
#. Services/Managers: implementing core business logic
#. Models/Providers: providing data through persistence layer or remote API interaction

In addition, we have the following helper layers:

#. Tools: generic functions with no need of object instantiation
#. Templates/Forms: generating output


.. figure:: _static/img/architecture_overview.png
   :scale: 50 %
   :alt: General system layout

   General system layout.

Implementation conventions
--------------------------
We try to implement classes in the several system layers along these general rules:

#. The controller layer should not talk to the models and providers directly
   but use service classes (usually called ``Managers``)
#. Models usually map to persistent database entities, but may also contain
   transient data types.  They do not call remote data providers, however -- this
   is handled by the provider classes.

Of course, rules may be broken -- but only if it makes the system easier to understand.