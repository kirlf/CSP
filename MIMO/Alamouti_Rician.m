clear all; close all; clc

snapshots = 100000;
EbNo = 0:10;
K = [4.0; 0.6];
M = [4; 8]; %Positions of modulation (M-PSK)
Mt = 2;
Mr = [1; 2];

ostbcEnc = comm.OSTBCEncoder('NumTransmitAntennas', Mt); % Alamouti

ric_ber = zeros(length(EbNo), length(M), length(K), length(Mr));
sum_BER = zeros(length(EbNo), length(M), length(K), length(Mr));


for mr = 1:length(Mr)
    ostbcComb = comm.OSTBCCombiner('NumTransmitAntennas', Mt, 'NumReceiveAntennas', Mr(mr));
    H = zeros(Mr(mr), Mt, snapshots);
    ric_msg = zeros(snapshots, Mr(mr));
    for k = 1:length(K)
        mu = sqrt( K(k)/(K(k)+1));
        s = sqrt(1/(K(k)+1));
        for m = 1:length(M)
        
            hModulator = comm.PSKModulator('ModulationOrder', M(m), 'BitInput', false); 
            hDemod = comm.PSKDemodulator('ModulationOrder', M(m), 'BitOutput', false);
            ric_ber(:,m,k,mr) = berfading(EbNo, 'psk', M(m), Mr(mr)*Mt, K(k));
        
            snr = EbNo+10*log10(log2(M(m)));
            message = randi([0,M(m)-1],100000,1);
    
            mod_msg = step(hModulator,message);
            Es = mean(abs(mod_msg).^2);

            alam_msg = step(ostbcEnc, mod_msg);

            % Channel
            h = mu + s*(1/sqrt(2))*(randn(Mr(mr),Mt,snapshots/Mt)...
            + 1j*randn(Mr(mr),Mt, snapshots/Mt));
            H(:,:,1:2:end-1) = h;
            H(:,:,2:2:end) = h;
            pathGainself = permute(H,[3,2,1]);

            % Transmit through the channel
            for q = 1:snapshots;  
                ric_msg(q,:) = (sqrt(Es/Mt)*H(:,:,q)*alam_msg(q,:).').';
            end

            for c = 1:100
                for jj = 1:length(EbNo)
                    noisy_mod = awgn(ric_msg,snr(jj),'measured','dB');
                    decodeData = step(ostbcComb,noisy_mod,pathGainself);
                    demod_msg = step(hDemod,decodeData);
                    [number,BER(c,jj)] = biterr(message,demod_msg);
                end
            end
            sum_BER(:,m, k, mr) = sum(BER)./c;
        end
    end
end

figure(1)

semilogy(EbNo,sum_BER(:,1,1,1),'r-o',EbNo,sum_BER(:,2,1,1),'g-o',...
         EbNo,ric_ber(:,1,1,1),'r-',EbNo,ric_ber(:,2,1,1),'g-',...
         EbNo,sum_BER(:,1,1,2),'b-o',EbNo,sum_BER(:,2,1,2),'y-o',...
         EbNo,ric_ber(:,1,1,2),'b-',EbNo,ric_ber(:,2,1,2),'y-',...
         'LineWidth', 1.5) 
title('Rician model (K = 4.0)') 
legend('QPSK(simulated) 2x1', '8-PSK(simulated) 2x1',...
    'QPSK(theory) 2x1','8-PSK(theory) 2x1',...
    'QPSK(simulated) 2x2', '8-PSK(simulated) 2x2',...
    'QPSK(theory) 2x2','8-PSK(theory) 2x2') 
xlabel('EbNo (dB)') 
ylabel('BER')
grid on


figure(2) 

semilogy(EbNo,sum_BER(:,1,2,1),'r-o',EbNo,sum_BER(:,2,2,1),'g-o',...
         EbNo,ric_ber(:,1,2,1),'r-',EbNo,ric_ber(:,2,2,1),'g-',...
         EbNo,sum_BER(:,1,2,2),'b-o',EbNo,sum_BER(:,2,2,2),'y-o',...
         EbNo,ric_ber(:,1,2,2),'b-',EbNo,ric_ber(:,2,2,2),'y-',...
         'LineWidth', 1.5) 
title('Rician model (K = 0.6)') 
legend('QPSK(simulated) 2x1', '8-PSK(simulated) 2x1',...
    'QPSK(theory) 2x1','8-PSK(theory) 2x1',...
    'QPSK(simulated) 2x2', '8-PSK(simulated) 2x2',...
    'QPSK(theory) 2x2','8-PSK(theory) 2x2')  
xlabel('EbNo (dB)') 
ylabel('BER')
grid on