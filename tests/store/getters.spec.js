import { expect } from 'chai';
import * as fc from 'fast-check';

import getters from '../../client/store/getters';
import storeState from '../../client/store/state';

describe('Store getters', () => {
    describe('authorizedGrant', () => {
        const { authorizedGrant } = getters;

        it('auth on default is false', () => {
            expect(authorizedGrant(storeState)).to.be.false;
        });

        it('is false when token is null', () => {
            fc.assert(fc.property(
                fc.string(1, 700),
                (token) => {
                    expect(authorizedGrant({ token: null })).to.be.false;
                },
            ));
        });

        it('is true when token are set', () => {
            fc.assert(fc.property(
                fc.string(1, 700),
                (token) => {
                    expect(authorizedGrant({ token })).to.be.true;
                },
            ));
        });
    });
});