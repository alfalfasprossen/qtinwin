This repo contains demo code for parenting a qt-widget (PySide) as a child to a native Windows window.  

I investigate this mainly concerning the problematic behaviour of PySide widgets created in 3dsMax (< v2017 probably) and Maya (not sure if this has been fixed in recent versions).
And of course just because we are able to do stuff like this.  

The code displays different variations of trying to achieve certain behaviours, maybe experimenting over-the-top (replacing the WndProc function from within python).  


#maxnativedialog
The first experiment for 3dsMax. It will create a native 3dsMax dialog window, which behaves correctly concerning z-ordering with sibling-windows. Then a PySide widget is parented into this dialog through native Windows functionality.


#maxparenting
*If you want to have code that might be usable for production, with a little fine-tuning on the event-filter, this is what you want.*
The second experiment, trying to circumvent the problems of having a native window around the qt widget.
By technically only setting the **owner** of the qt window to be the applications main window, this works pretty good out of the box.
> Note: there is a big difference between setting the owner and the parent of a windows window obviously. It is not documented very well in the win32 API, probably because you are generally only supposed to set the owner when you create a window with the appropriate function. Setting the **parent** will make the window a child or mdi-child that is confined to the area within the parent window. Setting the **owner** but not the parent, will let the window be a top-level window, the type of window all other 3dsMax 'child' windows are.


#mainwidget
Arbitrary experimenting code, not necessarily bound to any application. I actually started this by trying to parent a qt button into the windows text editor and then went on from there.
