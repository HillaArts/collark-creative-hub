const nodemailer = require('nodemailer');

async function sendConfirmationEmail(userEmail, bookingDetails) {
    let transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: 'your-email@gmail.com',
            pass: 'your-password',
        },
    });

    let info = await transporter.sendMail({
        from: '"Booking Confirmation" <no-reply@example.com>',
        to: userEmail,
        subject: 'Booking Confirmation',
        text: `Your appointment for ${bookingDetails.summary} has been confirmed for ${bookingDetails.startDateTime}.`,
        html: `<b>Your appointment for ${bookingDetails.summary} has been confirmed for ${bookingDetails.startDateTime}.</b>`,
    });

    console.log('Message sent: %s', info.messageId);
}