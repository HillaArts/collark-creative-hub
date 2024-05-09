const {google} = require('googleapis');
const calendar = google.calendar('v3');

async function addCalendarEvent(auth, eventDetails) {
    const calendarId = 'primary';
    const event = {
        summary: eventDetails.summary,
        description: eventDetails.description,
        start: {
            dateTime: eventDetails.startDateTime,
            timeZone: 'Kenya/Nairobi',
        },
        end: {
            dateTime: eventDetails.endDateTime,
            timeZone: 'Kenya/Nairobi',
        },
        // additional event details can be added here
    };

    try {
        const response = await calendar.events.insert({
            auth: auth,
            calendarId: calendarId,
            resource: event,
        });
        console.log('Event created: %s', response.data.htmlLink);
    } catch (error) {
        console.log('The API returned an error: ' + error);
    }
}