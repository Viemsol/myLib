# Spinix .rst Guide

## Heading

```code
*****
Title
*****

subtitle
########

subsubtitle
***********

this convention is used which you may want to follow :

# with overline, for parts
* with overline, for chapters
= for sections
- for subsections
^ for subsubsections
“ for paragraphs
```
and so on
use one asterisk on each side of a text you want to emphasize in italic and 2 asterisks in you want to make it **bold**
```code
*italic*
**bold**
```
double backquotes are used to make a text verbatim. For instance, it you want to use special characters such as *:
```code
This ``*`` character is not interpreted
```

## comments
comments can be made by adding two dots at the beginning of a line as follows:
```code
.. comments
```

## Replacring Long texts

```code
.. |longtext| replace:: this is a very very long text to include
```
and then insert |longtext| wherever needed.

##  colored boxes: note, seealso, todo and warnings
```code
.. seealso:: This is a simple **seealso** note. Other inline directive may be included (e.g., math :math:`\alpha`) but not al of them.
.. note:: This is a simple **note** note. Other inline directive may be included (e.g., math :math:`\alpha`) but not al of them.
.. warning:: This is a simple **warning** note. Other inline directive may be included (e.g., math :math:`\alpha`) but not al of them.
.. todo:: This is a simple **todo** note. Other inline directive may be included (e.g., math :math:`\alpha`) but not al of them.
```

## inserting code example
Literal code blocks are introduced by ending a paragraph with the special marker (double coulumn) ::. The literal block must be indented (and, like all paragraphs, separated from the surrounding ones by blank lines). default language is python
```code
This is a simple example::

    import math
    print 'import done'
```

you can specify the language using the code-block directive as follows:

```code
.. code-block:: html
    :linenos:

   <h1>code block example</h1>
```
## Plant UML

## Chart and graphs

## Images
```code
.. image:: ../images/test.png
    :width: 200pt
    :scale: 100%
.. image:: ../images/wiki_logo_openalea.png

.. image:: ../images/wiki_logo_openalea.png
    :width: 200px
    :align: center
    :height: 100px
    :alt: alternate text
```
## Figures
```code
.. figure:: ../images/wiki_logo_openalea.png
    :width: 200px
    :align: center
    :height: 100px
    :alt: alternate text
    :figclass: align-center

    figure are like images but with a caption

    and whatever else youwish to add

    .. code-block:: python

        import image
```

##  glossary
```code
:TBD: To be determined
```
another way
```code
.. glossary::

    apical
        at the top of the plant.
```

## Links
### Adding link internal to documet:
To add link 
```code
.. _test_link:

```

To refer link 
```code
:ref:`Link title <test_link>`
```

consider you need to refer any sub heading from paragraph, add link just above subheading (Note **no uppercase letters**)
```code
.. _firmware_image_header:

Firmware Image Header 
^^^^^^^^^^^^^^^^^^^^^^
```
Then add below to access link  in paragraph
```code
Refer :ref:`Firmware Image Header <firmware_image_header>`
```
 
### Adding External Link:
`CNN <http://cnn.com>`_  
### Adding link to typedef: (get relatice ink and add from doxygen document)
`CNN2 <api.html#c.fwImageValidate_t>`_

## Auto Numbering
```code
1. Thi is 

#. About

#. Auto numbering
```
## Unordered Lists
```code
1. Thi is 
    * Item 1.

    * Item 2.
#. About
    * Item 1.

    * Item 2.
#. Auto numbering
```
## Tables 
```code
.. list-table:: Firmware Image structure
   :widths: 25 25 50
   :header-rows: 1

   * - Components
     - Size in Bytes
     - Description
   * - Firmware Image Header
     - 48
     - Refer fwImageHeader_t for content.
   * - Project data
     - Size specified in fwImageHeader_t
     - Used for storing Image Signature information. 
```