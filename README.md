This repo contains demo code for parenting a qt-widget (PySide) as a child to a native Windows window.

I investigate this mainly concerning the problematic behaviour of PySide widgets created in 3dsMax (< v2017 probably) and Maya (not sure if this has been fixed in recent versions).
And of course just because we are able to do stuff like this.

The current demo code is for 3dsMax. It will create a native 3dsMax dialog window, which behaves correctly concerning z-ordering with sibling-windows. Then a PySide widget is parented into this dialog through native Windows functionality.
