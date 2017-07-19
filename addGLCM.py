import gi

from GLCM import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="DWTGLCMPSNR")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box1)
        self.loadimg = Gtk.Image.new_from_file('')
        self.loadimg.set_pixel_size(200)
        box1.pack_start(self.loadimg, 1, 1, 10)
        box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box1.pack_start(box2, 1, 1, 10)
        self.imgbuffer = Gtk.TextBuffer()
        self.img = Gtk.TextView()
        self.img.set_buffer(self.imgbuffer)
        self.imgbuffer.set_text("")
        self.img.set_can_focus(0)
        box2.pack_start(self.img, 1, 1, 10)

        filechooser = Gtk.Button(label="...")
        filechooser.connect("clicked", self.on_image_clicked)
        box2.pack_start(filechooser, 0, 0, 5)
        self.progress_bar = Gtk.ProgressBar()
        box1.pack_start(self.progress_bar, 1, 1, 0)
        bttndwt = Gtk.Button(label="Add to Databse")
        bttndwt.connect("clicked", self.on_bttndwt_clicked)
        box1.pack_start(bttndwt, 1, 1, 0)

    def on_bttndwt_clicked(self, widget):
        image = cv2.imread(self.imgbuffer.get_text(
            self.imgbuffer.get_iter_at_line(0), self.imgbuffer.get_iter_at_offset(-1), 0))
        glcmimage = GLCM(image,0,1)
        glcmimage.printglcm();
        glcmimage.writeglcm();



    def on_image_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Pilih Gambar ", self, Gtk.FileChooserAction.OPEN, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.imgbuffer.set_text(dialog.get_filename())
            self.loadimg.set_from_file(dialog.get_filename())
            self.resize(400, 200)
            print("File Selected", dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_image = Gtk.FileFilter()
        filter_image.set_name("Image File")
        filter_image.add_mime_type("image/*")
        dialog.add_filter(filter_image)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


if __name__ == '__main__':
    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
