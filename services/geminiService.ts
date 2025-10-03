import { GoogleGenAI, Type } from '@google/genai';
import { Pet, Service } from '../types';

// IMPORTANT: This check is to prevent crashing in environments where process.env is not defined.
const apiKey = typeof process !== 'undefined' && process.env && process.env.API_KEY
  ? process.env.API_KEY
  : undefined;

if (!apiKey) {
    console.error("API_KEY environment variable not set.");
}

const ai = new GoogleGenAI({ apiKey: apiKey || '' });

const petSchema = {
    type: Type.ARRAY,
    items: {
      type: Type.OBJECT,
      properties: {
        id: { type: Type.STRING, description: 'A unique identifier for the pet, e.g., pet_01' },
        name: { type: Type.STRING, description: 'The pet\'s name.' },
        species: { type: Type.STRING, description: 'The species of the pet (Dog, Cat, Bird, Other).' },
        breed: { type: Type.STRING, description: 'The pet\'s breed.' },
        age: { type: Type.NUMBER, description: 'The pet\'s age in years.' },
        description: { type: Type.STRING, description: 'A detailed paragraph about the pet\'s personality and background.' },
        quickFacts: { type: Type.ARRAY, items: { type: Type.STRING }, description: 'A list of 3-4 short, fun facts about the pet.' },
      },
      required: ['id', 'name', 'species', 'breed', 'age', 'description', 'quickFacts'],
    },
};

const serviceSchema = {
    type: Type.ARRAY,
    items: {
        type: Type.OBJECT,
        properties: {
            id: { type: Type.STRING, description: 'Unique ID for the service, e.g., service_01' },
            name: { type: Type.STRING, description: 'Name of the service.' },
            description: { type: Type.STRING, description: 'A short description of the service.' },
            price: { type: Type.NUMBER, description: 'Price of the service in USD.' },
        },
        required: ['id', 'name', 'description', 'price'],
    }
};


export const generatePetsData = async (): Promise<Omit<Pet, 'imageUrls'>[]> => {
    if (!apiKey) return Promise.resolve([]);
    try {
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: 'Generate a list of 12 diverse and fictional pets available for adoption. Include dogs, cats, birds, and other small animals. Give them unique personalities.',
            config: {
                responseMimeType: 'application/json',
                responseSchema: petSchema,
            },
        });

        return JSON.parse(response.text);

    } catch (error) {
        console.error('Error generating pet data:', error);
        return [];
    }
};

export const generateServicesData = async (): Promise<Omit<Service, 'imageUrl'>[]> => {
    if (!apiKey) return Promise.resolve([]);
    try {
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: 'Generate a list of 5 common pet care services, like grooming, checkups, and training.',
            config: {
                responseMimeType: 'application/json',
                responseSchema: serviceSchema,
            },
        });

        return JSON.parse(response.text);

    } catch (error) {
        console.error('Error generating service data:', error);
        return [];
    }
};