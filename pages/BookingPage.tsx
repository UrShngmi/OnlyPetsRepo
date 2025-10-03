import React, { useState, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAppContext } from '../contexts/AppContext';
import LoadingSpinner from '../components/LoadingSpinner';
import Breadcrumbs from '../components/Breadcrumbs';
import { Booking } from '../types';

const BookingPage: React.FC = () => {
  const { type, id } = useParams<{ type: 'pet' | 'service'; id: string }>();
  const { pets, services, loading, addToast, bookings, addBooking } = useAppContext();
  const navigate = useNavigate();

  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState({
    // Personal Info
    name: '',
    email: '',
    phone: '',
    // Adoption Info
    adoptionReason: '',
    homeEnvironment: '',
    // Service Info
    petName: '',
    petBreed: '',
    specialNotes: '',
    // Scheduling
    appointmentDate: '',
    appointmentTime: '',
  });
  const [calendarDate, setCalendarDate] = useState(new Date());

  const item = useMemo(() => {
    if (type === 'pet') return pets.find(p => p.id === id);
    return services.find(s => s.id === id);
  }, [pets, services, type, id]);

  const isPetAdoption = type === 'pet';
  
  const adoptionSteps = ['Personal Info', 'Adoption Survey', 'Review Application', 'Confirmation'];
  const serviceSteps = ['Personal Info', 'Schedule', 'Booking Details', 'Review & Confirm', 'Confirmation'];
  const steps = isPetAdoption ? adoptionSteps : serviceSteps;

  if (loading) return <LoadingSpinner />;
  if (!item) {
    return <div className="text-center text-red-500">Item not found.</div>;
  }

  const handleNext = (e: React.FormEvent) => {
    e.preventDefault();
    if (step < steps.length - 2) { // Move to next form step or review step
      setStep(step + 1);
    } else { // Handle final submission from review step
      if (isPetAdoption) {
         // In a real app, you'd send formData to a server here.
      } else {
        const newBooking: Booking = {
            serviceId: item.id,
            date: formData.appointmentDate,
            timeSlot: formData.appointmentTime as 'morning' | 'afternoon',
        };
        addBooking(newBooking);
      }
       setStep(step + 1); // Move to the confirmation screen
    }
  };

  const handleBack = () => {
    if (step > 0) {
      setStep(step - 1);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  
  const renderScheduler = () => {
    const year = calendarDate.getFullYear();
    const month = calendarDate.getMonth();
    const firstDayOfMonth = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const handleDateSelect = (day: number) => {
        const date = new Date(year, month, day);
        if (date < new Date(new Date().toDateString())) return; // Disable past dates
        const isoDate = date.toISOString().split('T')[0]; // YYYY-MM-DD
        setFormData(prev => ({ ...prev, appointmentDate: isoDate, appointmentTime: '' }));
    };

    const handleTimeSelect = (time: 'morning' | 'afternoon') => {
        setFormData(prev => ({...prev, appointmentTime: time}));
    };
    
    const isSlotBooked = (time: 'morning' | 'afternoon') => {
        if (!formData.appointmentDate) return false;
        return bookings.some(
            b => b.serviceId === id && b.date === formData.appointmentDate && b.timeSlot === time
        );
    };

    const calendarDays = [];
    for (let i = 0; i < firstDayOfMonth; i++) {
        calendarDays.push(<div key={`empty-${i}`} className="w-10 h-10"></div>);
    }
    for (let day = 1; day <= daysInMonth; day++) {
        const fullDateStr = new Date(year, month, day).toISOString().split('T')[0];
        const isSelected = formData.appointmentDate === fullDateStr;
        const isPast = new Date(year, month, day) < new Date(new Date().toDateString());

        calendarDays.push(
            <button
                type="button"
                key={day}
                onClick={() => handleDateSelect(day)}
                disabled={isPast}
                className={`w-10 h-10 flex items-center justify-center rounded-full transition-colors ${
                    isSelected ? 'bg-yellow-500 text-black font-bold' 
                    : isPast ? 'text-gray-600 cursor-not-allowed'
                    : 'hover:bg-gray-700'
                }`}
            >
                {day}
            </button>
        );
    }

    return (
        <div>
            <div className="flex items-center justify-between mb-4">
                <button type="button" onClick={() => setCalendarDate(new Date(year, month - 1, 1))} className="p-2 rounded-full hover:bg-gray-700 transition-colors">&lt;</button>
                <h3 className="text-lg font-semibold text-white">{calendarDate.toLocaleString('default', { month: 'long', year: 'numeric' })}</h3>
                <button type="button" onClick={() => setCalendarDate(new Date(year, month + 1, 1))} className="p-2 rounded-full hover:bg-gray-700 transition-colors">&gt;</button>
            </div>
            
            <div className="grid grid-cols-7 gap-2 text-center">
                {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map(d => <div key={d} className="w-10 h-10 flex items-center justify-center font-bold text-gray-500 text-sm">{d}</div>)}
                {calendarDays}
            </div>

            {formData.appointmentDate && (
                <div className="mt-6 pt-6 border-t border-gray-700">
                    <h4 className="font-semibold mb-3 text-white">Select a Time Slot for {formData.appointmentDate}</h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <button type="button" disabled={isSlotBooked('morning')} onClick={() => handleTimeSelect('morning')} className={`p-4 rounded-lg border-2 text-left transition-colors disabled:opacity-50 disabled:cursor-not-allowed disabled:border-gray-700 disabled:text-gray-500 ${formData.appointmentTime === 'morning' ? 'bg-yellow-500 border-yellow-500 text-black' : 'border-gray-600 hover:border-yellow-500 text-white'}`}>
                            <p className="font-bold">Morning</p>
                            <p className="text-sm">9:00 AM - 12:00 PM</p>
                        </button>
                         <button type="button" disabled={isSlotBooked('afternoon')} onClick={() => handleTimeSelect('afternoon')} className={`p-4 rounded-lg border-2 text-left transition-colors disabled:opacity-50 disabled:cursor-not-allowed disabled:border-gray-700 disabled:text-gray-500 ${formData.appointmentTime === 'afternoon' ? 'bg-yellow-500 border-yellow-500 text-black' : 'border-gray-600 hover:border-yellow-500 text-white'}`}>
                            <p className="font-bold">Afternoon</p>
                            <p className="text-sm">1:00 PM - 5:00 PM</p>
                        </button>
                    </div>
                     {isSlotBooked('morning') && <p className="text-red-400 text-sm mt-2">The morning slot is unavailable on this date.</p>}
                     {isSlotBooked('afternoon') && <p className="text-red-400 text-sm mt-2">The afternoon slot is unavailable on this date.</p>}
                </div>
            )}
        </div>
    );
  }

  const renderFormStep = (stepIndex: number) => {
    if (isPetAdoption) {
        switch (stepIndex) {
            case 0: // Personal Info
                return (
                    <div className="space-y-4">
                         <h3 className="text-xl font-bold text-white mb-4">Your Contact Information</h3>
                         <input type="text" name="name" placeholder="Full Name" value={formData.name} onChange={handleChange} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
                         <input type="email" name="email" placeholder="Email Address" value={formData.email} onChange={handleChange} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
                         <input type="tel" name="phone" placeholder="Phone Number" value={formData.phone} onChange={handleChange} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
                    </div>
                );
            case 1: // Adoption Survey
                return (
                    <div className="space-y-6">
                        <h3 className="text-xl font-bold text-white mb-4">Tell Us About Yourself</h3>
                        <textarea name="adoptionReason" placeholder="Why are you looking to adopt a pet at this time?" rows={4} value={formData.adoptionReason} onChange={handleChange} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
                        <textarea name="homeEnvironment" placeholder="Describe your home environment (e.g., apartment, house with yard, other pets, children)." rows={4} value={formData.homeEnvironment} onChange={handleChange} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
                    </div>
                );
            case 2: // Review
                return (
                    <div className="space-y-3 text-gray-300 bg-[#2a2a2a] p-6 rounded-lg">
                        <h3 className="text-xl font-bold text-white border-b border-gray-700 pb-2 mb-4">Confirm Your Details</h3>
                        <p><strong>Applying to Adopt:</strong> {item.name}</p>
                        <div className="border-t border-gray-700 my-2"></div>
                        <p><strong>Name:</strong> {formData.name}</p>
                        <p><strong>Email:</strong> {formData.email}</p>
                        <p><strong>Phone:</strong> {formData.phone}</p>
                        <div className="border-t border-gray-700 my-2"></div>
                        <p><strong>Reason for Adopting:</strong> {formData.adoptionReason || 'N/A'}</p>
                        <p><strong>Home Environment:</strong> {formData.homeEnvironment || 'N/A'}</p>
                    </div>
                );
            default: return null;
        }
    } else { // Service Booking Flow
        switch (stepIndex) {
            case 0: // Personal Info
                 return (
                    <div className="space-y-4">
                         <h3 className="text-xl font-bold text-white mb-4">Your Contact Information</h3>
                         <input type="text" name="name" placeholder="Full Name" value={formData.name} onChange={handleChange} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
                         <input type="email" name="email" placeholder="Email Address" value={formData.email} onChange={handleChange} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
                         <input type="tel" name="phone" placeholder="Phone Number" value={formData.phone} onChange={handleChange} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
                    </div>
                );
            case 1: // Scheduler
                return renderScheduler();
            case 2: // Booking Details
                return (
                     <div className="space-y-4">
                        <h3 className="text-xl font-bold text-white mb-4">Tell Us About Your Pet</h3>
                         <input type="text" name="petName" placeholder="Pet's Name" value={formData.petName} onChange={handleChange} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
                         <input type="text" name="petBreed" placeholder="Pet's Breed" value={formData.petBreed} onChange={handleChange} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
                         <textarea name="specialNotes" placeholder="Any special notes or instructions for our staff? (e.g., allergies, behavior quirks)" rows={4} value={formData.specialNotes} onChange={handleChange} className="w-full bg-[#2a2a2a] text-white p-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500" />
                    </div>
                );
            case 3: // Review
                return (
                    <div className="space-y-3 text-gray-300 bg-[#2a2a2a] p-6 rounded-lg">
                        <h3 className="text-xl font-bold text-white border-b border-gray-700 pb-2 mb-4">Confirm Your Booking</h3>
                        <p><strong>Service:</strong> {item.name}</p>
                        <p><strong>Appointment:</strong> {formData.appointmentDate} <span className="capitalize">({formData.appointmentTime})</span></p>
                        <div className="border-t border-gray-700 my-2"></div>
                        <p><strong>Your Name:</strong> {formData.name}</p>
                        <p><strong>Contact:</strong> {formData.email}</p>
                         <div className="border-t border-gray-700 my-2"></div>
                        <p><strong>Pet Name:</strong> {formData.petName}</p>
                        <p><strong>Pet Breed:</strong> {formData.petBreed}</p>
                        <p><strong>Notes:</strong> {formData.specialNotes || 'None'}</p>
                    </div>
                );
            default: return null;
        }
    }
  };

  const isNextDisabled = () => {
    if (step === 0 && (!formData.name || !formData.email || !formData.phone)) return true;
    if (isPetAdoption) {
        if (step === 1 && (!formData.adoptionReason || !formData.homeEnvironment)) return true;
    } else {
        if (step === 1 && (!formData.appointmentDate || !formData.appointmentTime)) return true;
        if (step === 2 && (!formData.petName || !formData.petBreed)) return true;
    }
    return false;
  }

  const getButtonText = () => {
      if (step === steps.length - 2) return 'Confirm & Submit';
      return 'Next Step';
  }

  const isConfirmationStep = step === steps.length - 1;

  return (
    <div>
       <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-2">{isPetAdoption ? 'Adoption Application' : 'Book a Service'}</h1>
        {!isConfirmationStep && <p className="text-lg text-gray-400">You're applying for: <span className="text-yellow-400 font-semibold">{item.name}</span></p>}
      </div>

      <div className="max-w-4xl mx-auto bg-[#121212] p-8 md:p-12 rounded-3xl">
        <div className="mb-12">
            <Breadcrumbs steps={steps} currentStep={step} />
        </div>

        {isConfirmationStep ? (
             <div className="text-center py-10">
                <div className="w-24 h-24 mx-auto mb-6 flex items-center justify-center rounded-full bg-green-500 bg-opacity-20">
                     <svg className="h-12 w-12 text-green-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                </div>
                <h2 className="text-3xl font-bold text-white mb-4">{isPetAdoption ? 'Application Submitted!' : 'Booking Confirmed!'}</h2>
                <p className="text-gray-300 max-w-md mx-auto mb-8">
                    {isPetAdoption 
                    ? `Thank you for your interest in adopting ${item.name}. We have received your application and will contact you within 3-5 business days to discuss the next steps.`
                    : `Your appointment for ${item.name} on ${formData.appointmentDate} (${formData.appointmentTime}) is confirmed. We look forward to seeing you and ${formData.petName}!`}
                </p>
                <button onClick={() => navigate('/')} className="bg-yellow-500 text-black font-bold py-3 px-8 rounded-lg hover:bg-yellow-400 transition-colors">
                    Back to Homepage
                </button>
            </div>
        ) : (
            <form onSubmit={handleNext}>
                <div className="min-h-[300px]">
                    {renderFormStep(step)}
                </div>
                <div className="mt-12 flex justify-between items-center">
                    <button 
                        type="button" 
                        onClick={handleBack} 
                        disabled={step === 0}
                        className="bg-gray-600 text-white font-bold py-3 px-8 rounded-lg hover:bg-gray-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Back
                    </button>
                    <button 
                        type="submit" 
                        disabled={isNextDisabled()}
                        className="bg-yellow-500 text-black font-bold py-3 px-8 rounded-lg hover:bg-yellow-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-gray-500"
                    >
                        {getButtonText()}
                    </button>
                </div>
            </form>
        )}
      </div>
    </div>
  );
};

export default BookingPage;