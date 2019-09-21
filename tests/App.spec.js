import { mount } from '@vue/test-utils';
import App from '../yumljira/templates/App.vue';

const wrapper = mount(App);

describe('MyName test', () => {
    it('Displays my name when I write it', () => { 
        expect(wrapper.vm.$data.name).toBe('My name');
    
        const input = wrapper.find('input');
        input.element.value = 'Kamil';
        input.trigger('input');
    
        expect(wrapper.vm.$data.name).toBe('Kamil');
    })
});
