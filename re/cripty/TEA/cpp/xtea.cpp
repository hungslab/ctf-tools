#include <stdio.h>
#include <stdint.h>
 
/* take 64 bits of data in v[0] and v[1] and 128 bits of key[0] - key[3] */
 
void encrypt(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) {
    unsigned int i;
    uint32_t v0=v[0], v1=v[1], sum=0, delta=0x9E3779B9;
    for (i=0; i < num_rounds; i++) {
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
        sum += delta;
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
    }
    v[0]=v0; v[1]=v1;
}
 
void decrypt(unsigned int num_rounds, uint32_t *v, uint32_t const *key) {
    unsigned int i;
    uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*num_rounds;
    for (i=0; i < num_rounds; i++) {
        v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
        sum -= delta;
        v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
    }
    v[0]=v0; v[1]=v1;
}
 
int main()
{
	uint32_t enflag[] = {0x0B3D9DA5, 0x2862A369, 0X9626BD78};
	uint32_t key[4] = {2, 0, 2, 4};
	unsigned int round = 36;
    for(int i=0;i<sizeof(enflag)/sizeof(enflag[0]);i+=2)
    {
        uint32_t temp[2];
        temp[0] = enflag[i];
        temp[1] = enflag[i+1];
        decrypt(round, temp, key);
        // decrypt(round, temp, key);
//		printf("%08X%08X",temp[0],temp[1]);
        printf("%c%c%c%c%c%c%c%c",*((char*)&temp[0]+0),*((char*)&temp[0]+1),*((char*)&temp[0]+2),*((char*)&temp[0]+3),*((char*)&temp[1]+0),*((char*)&temp[1]+1),*((char*)&temp[1]+2),*((char*)&temp[1]+3));
//    	printf("%02x%02x%02x%02x%02x%02x%02x%02x",*((char*)&temp[0]+0),*((char*)&temp[0]+1),*((char*)&temp[0]+2),*((char*)&temp[0]+3),*((char*)&temp[1]+0),*((char*)&temp[1]+1),*((char*)&temp[1]+2),*((char*)&temp[1]+3));
    }
    return 0;
}