import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap
import qrcode
from contact_card_ui import Ui_vCardQRCodegenerator  # Updated QMainWindow name

# Function to create vCard from user input
def create_vcard(full_name, phone_number, email):
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{full_name}
TEL:{phone_number}
EMAIL:{email}

END:VCARD"""
    return vcard

# Main application class
class ContactCardApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ContactCardApp, self).__init__()
        self.ui = Ui_vCardQRCodegenerator()  # Updated QMainWindow name
        self.ui.setupUi(self)

        # Set window flags to remove the title bar and frame
        # self.setWindowFlags(Qt.FramelessWindowHint)

        self.setFixedSize(768, 769)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Connect buttons to their respective functions
        self.ui.genvcard.clicked.connect(self.generate_vcard)  # Button to generate vCard
        self.ui.GenerateQRCode.clicked.connect(self.generate_qr_code)  # Button to generate QR code
        self.ui.reset.clicked.connect(self.reset_fields)  # Button to reset fields
        self.ui.exit.clicked.connect(self.exit_program)  # Button to exit program

      
    def generate_vcard(self):
        # Get the input data from the UI fields
        full_name = self.ui.fullname.text()  # Name textbox
        phone_number = self.ui.number.text()  # Phone number textbox
        email = self.ui.email.text()  # Email textbox
       

        # Create the vCard and display it in the text box
        vcard_data = create_vcard(full_name, phone_number, email )
        self.ui.vcardoutput.setPlainText(vcard_data)  # Show the vCard in the QTextEdit

    def generate_qr_code(self):
        # Generate vCard first
        full_name = self.ui.fullname.text()  # Name textbox
        phone_number = self.ui.number.text()  # Phone number textbox
        email = self.ui.email.text()  # Email textbox
        

        vcard_data = create_vcard(full_name, phone_number, email )

        # Create the QR code from the vCard data
        qr = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4
        )
        qr.add_data(vcard_data)
        qr.make(fit=True)

        # Save the QR code as an image
        qr_image_path = "contact_qr_code.png"
        img = qr.make_image(fill="black", back_color="white")
        img.save(qr_image_path)


        # Load the image into QPixmap and scale it to fit [431, 261]
        pixmap = QPixmap(qr_image_path)
        scaled_pixmap = pixmap.scaled(431, 261, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        # Display the scaled QR code in the QLabel
        self.ui.QRcodeoutput.setPixmap(scaled_pixmap)

        
        # Display the QR code in the QLabel
        pixmap = QPixmap(qr_image_path)
        self.ui.QRcodeoutput.setPixmap(pixmap)  # Updated QLabel name

    def reset_fields(self): 
         # Clear all input fields
        self.ui.fullname.clear()  # Name textbox
        self.ui.number.clear()  # Phone number textbox
        self.ui.email.clear()  # Email textbox
        
    
        # Clear vCard output
        self.ui.vcardoutput.clear()  # QTextEdit for vCard output
    
        # Clear QR code output
        self.ui.QRcodeoutput.clear()  # QLabel for QR code


    def exit_program(self):
         # Close the application
        self.close()


    # Run the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = ContactCardApp()
    main_window.show()
    sys.exit(app.exec_())    