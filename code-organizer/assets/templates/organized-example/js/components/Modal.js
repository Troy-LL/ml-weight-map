/**
 * Modal Component
 * Reusable modal dialog
 */

import { $ } from './utils.js';

export class Modal {
    constructor(content) {
        this.content = content;
        this.isOpen = false;
        this.element = null;
    }

    open() {
        if (this.isOpen) return;

        this.element = this.create();
        document.body.appendChild(this.element);
        this.isOpen = true;

        // Add event listeners
        const closeBtn = this.element.querySelector('.modal__close');
        closeBtn?.addEventListener('click', () => this.close());
    }

    close() {
        if (!this.isOpen) return;

        this.element?.remove();
        this.element = null;
        this.isOpen = false;
    }

    create() {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
      <div class="modal__overlay"></div>
      <div class="modal__content">
        <button class="modal__close">&times;</button>
        <div class="modal__body">${this.content}</div>
      </div>
    `;
        return modal;
    }
}
