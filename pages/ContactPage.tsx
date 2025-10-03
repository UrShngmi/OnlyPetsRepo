import React from 'react';

const ContactPage: React.FC = () => {
  return (
    <div>
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-2">Get In Touch</h1>
        <p className="text-lg text-gray-400">We'd love to hear from you!</p>
      </div>
      <div className="bg-[#121212] p-8 md:p-12 rounded-3xl grid grid-cols-1 md:grid-cols-2 gap-12">
        <div>
            <h2 className="text-3xl font-bold text-white mb-6">Send us a Message</h2>
            <form className="space-y-4">
                <input type="text" placeholder="Your Name" className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" />
                <input type="email" placeholder="Your Email" className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" />
                <textarea placeholder="Your Message" rows={5} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500"></textarea>
                <button type="submit" className="w-full bg-yellow-500 text-black font-bold py-3 rounded-lg hover:bg-yellow-400 transition-colors">
                    Send Message
                </button>
            </form>
        </div>
        <div>
            <h2 className="text-3xl font-bold text-white mb-6">Our Location</h2>
            <div className="bg-[#2a2a2a] h-64 rounded-lg flex items-center justify-center text-gray-400">
                [Map Placeholder - 123 Pet Lane, Animal City]
            </div>
            <div className="mt-6 text-gray-300 space-y-2">
                <p><strong>Email:</strong> contact@onlypets.com</p>
                <p><strong>Phone:</strong> (123) 456-7890</p>
                <p><strong>Hours:</strong> Mon - Sat, 9am - 6pm</p>
            </div>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;
