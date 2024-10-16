#include<stdio.h>
#include<stdint.h>
#define MX (((z>>5^y<<2)+(y>>3^z<<4))^((sum^y)+(key[(p&3)^e]^z)))
// #define MX 0x61C88647
//#define MX (((z>>4^y<<2)+(y>>3^z<<5))^((sum^y)+(key[(e^p&3)]^z)))
#define DELTA 0x9e3779b9
//#define DELTA 0x11451400
//delta=0x61C88647=-(0x9e3779b)

//加密
void xxtea(uint32_t* v,int n,uint32_t const key[4]){
	uint32_t y,z,sum;
	unsigned p,rounds,e;
	if(n>1){
		rounds=6+52/n;
		sum=0;
		z=v[n-1];
		do{
			sum+=DELTA;
			e=(sum>>2)&3;
			for(p=0;p<n-1;p++){
				y=v[p+1];
				v[p]+=MX;
				z=v[p];
			}
			y=v[0];
			v[n-1]+=MX;
			z=v[n-1];
		}
		while(--rounds);
	}
	else if(n<-1){
		n=-n;
		rounds=6+52/n;
		sum=DELTA*rounds;
		y=v[0];
		do{
			e=(sum>>2)&3;
			for(p=n-1;p>0;p--){
				z=v[p-1];
				v[p]-=MX;
				y=v[p];
			}
			z=v[n-1];
			v[0]-=MX;
			y=v[0];
			sum-=DELTA;
		}
		while(--rounds);
	}
}

int main(){
	//uint32_t v[]={0x64F5E178, 0xE1F035A8, 0x34FF1205, 0xFB13E9B0, 0x50A3B989, 0xB1DA43C9, 0x4FC8DB01,0x20DB16AF, 0xED671796};

	uint32_t v[]={0x78E1F564, 0xA835F0E1, 0x0512FF34, 0xB0E913FB, 0x89B9A350, 0xC943DAB1, 0x01DBC84F,
	0xAF16DB20, 0x961767ED};
	uint32_t const k[4]={0x6d6f6563, 0x74663230, 0x32342121, 0xCCFFBBBB};
//	n=bit(v)/32,正数表示加密,负数表示解密
	int n=sizeof(v)/sizeof(v[0]);
	printf("n = %d\n",n);
//	v:明文 ___bit
//	k:密钥 128bit
//	printf("明文:%u %u\n",v[0],v[1]);
//	xxtea(v,n,k);
//	printf("加密后:\n");
//	for(int i=0;i<n;i++){
//		printf("%8x",v[i]);
//	}
	xxtea(v,-n,k);
	printf("解密后:\n");
//	for(int i=0;i<n;i++){
//		printf("%8x",v[i]);
//	}
	for(int i=0;i<n;i++){
		printf("%c%c%c%c",v[i]&0xff,(v[i]>>8)&0xff,(v[i]>>16)&0xff,(v[i]>>24)&0xff);
	}
}