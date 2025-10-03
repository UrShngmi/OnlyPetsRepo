import { Pet, Service } from '../types';

const generateSeed = (id: string) => {
    return id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
}

export const getPetImages = (pet: Omit<Pet, 'imageUrls'>): string[] => {
    const seed = generateSeed(pet.id);
    const images = [];
    const baseSize = 400;

    for (let i = 0; i < 4; i++) {
        let url;
        const size = baseSize + i * 10;
        const currentSeed = `${seed + i}`;
        switch(pet.species) {
            case 'Dog':
                 url = `https://placedog.net/${size}/${size}?random=${currentSeed}`;
                break;
            case 'Cat':
                url = `https://placekitten.com/${size}/${size}?image=${(seed + i) % 16}`;
                break;
            case 'Bird':
                url = `https://picsum.photos/seed/${currentSeed}-bird/${size}`;
                break;
            default:
                url = `https://picsum.photos/seed/${currentSeed}-pet/${size}`;
        }
        images.push(url);
    }
    return images;
};

export const getServiceImage = (service: Omit<Service, 'imageUrl'>): string => {
    const seed = generateSeed(service.id);
    const name = service.name.toLowerCase();

    if (name.includes('grooming')) return `https://picsum.photos/seed/${seed}-grooming/600/400`;
    if (name.includes('training')) return `https://picsum.photos/seed/${seed}-training/600/400`;
    if (name.includes('health') || name.includes('vet')) return `https://picsum.photos/seed/${seed}-vet/600/400`;
    if (name.includes('walking')) return `https://picsum.photos/seed/${seed}-walking/600/400`;
    
    return `https://picsum.photos/seed/${seed}-service/600/400`;
};
