/**
 * Main Application Entry Point
 * Handles initialization and setup
 */

import { $ } from './utils.js';
import { Modal } from './components/Modal.js';

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('App initialized');

    // Example: Button click handler
    const demoBtn = $('#demoBtn');
    if (demoBtn) {
        demoBtn.addEventListener('click', handleDemoClick);
    }
});

function handleDemoClick() {
    const modal = new Modal('<h3>Hello!</h3><p>This is a well-organized project.</p>');
    modal.open();
}
