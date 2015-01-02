======================
Database Configuration
======================

After you have installed Connect, but before you start inviting new users, you will need to configure a few things in the database.

First - login to the Django admin using your ``superuser`` credentials.


Sites [Required]
________________

In addition to using the Django sites framework, Connect **requires** you to specify a number of additional settings used throughout the site and email templates:

* A logo
* A site tagline
* An email address for receiving enquiries (for example, if a member wishes to challenge a moderator's decision)
* An email header image


Brands
______

If you are setting up a site for artists, you might anticipate that many of your members have a Deviant Art page.
In this case, you would register:

* ``Deviant Art`` as the ``brand name``
* ``deviantart.com`` as the ``domain``
* ``fa-deviantart`` as the ``font awesome icon``

Now, when a member adds ``http://deviantart.com/mypage/`` to their public profile, the icon *next* to that link will be the font awesome deviant art icon.


Roles
_____

Roles define how a member would like to interact with others in the community.
For example, an artist community might want to set up the following roles:

1.  ``Social`` with the description ``I would like to socialise with other members``
2.  ``Share Materials`` with the description ``I would like to share art materials with other members``
3.  ``Share Workshop`` with the description ``I would like to share a workshop space with other members``
4.  ``Exhibition Partner`` with the description ``I would like to do joint exhibitions with other members``
5.  ``Mentor`` with the description ``I would like to mentor other members``


Once roles are set up in the database, members can:

* Select one or more role to display on their public profile
* Search the membership base by one or more role


Skills
______

Skills allow members to indicate their areas of expertise and interest.
If you were setting up an art community, skills could include:

* Sculpture
* Installation Art
* Watercolors
* Oils
* Vector Art
* Photography

Once skills are set up in the database, members can:

* Select one or more skill to display on their public profile
* Specify a proficiency for each skill displayed on their public profile
* Search the membership base by one or more skill


.. note::
    Creating the skills via the Django admin (rather than allowing members to create skills on the fly) is a deliberate
    design decision - as it avoids the creation of similar or duplicate skills.
    If a member wants to list a skill that is not available, Connect invites them to email the email address set in your ``site`` configuration.
    **Choose your skills wisely!**


Flat Pages
__________

Pages added via Flat Pages are automatically added to the site-wide footer.
Example pages to consider:

* Code of Conduct
* Privacy Policy
* Terms and Conditions
