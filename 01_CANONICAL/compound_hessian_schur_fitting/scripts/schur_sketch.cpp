#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <tuple>
#include <unordered_map>
#include <utility>
#include <vector>
#ifdef _OPENMP
#include <functional>
#include <omp.h>
#endif

using Perm = std::array<uint8_t,6>;
struct Entry { uint32_t key; int32_t val; };
struct Row { uint8_t a,b; std::vector<Entry> e; };
struct Term { Perm p; int coeff; };

static uint64_t splitmix64(uint64_t x){
  x += 0x9e3779b97f4a7c15ULL;
  x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
  x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
  return x ^ (x >> 31);
}
static int modnorm(long long x,int p){ x%=p; if(x<0)x+=p; return (int)x; }
static int modpow(int a,int e,int p){ long long r=1,b=a; while(e){if(e&1)r=r*b%p;b=b*b%p;e>>=1;}return (int)r; }

static void read_exact(std::ifstream& f,char* dst,std::streamsize n,const char* label){
  f.read(dst,n); if(f.gcount()!=n) throw std::runtime_error(std::string("truncated ")+label);
}
static std::vector<Row> read_rows(const std::string& path){
  std::ifstream f(path,std::ios::binary); if(!f) throw std::runtime_error("cannot open "+path);
  const char expected[8]={'R','H','T','6','v','1','\0','\0'}; char magic[8];
  read_exact(f,magic,8,"magic"); if(!std::equal(magic,magic+8,expected)) throw std::runtime_error("bad magic");
  uint32_t n=0,nrows=0; read_exact(f,(char*)&n,4,"n"); read_exact(f,(char*)&nrows,4,"nrows");
  if(n!=16 || (nrows!=136 && nrows!=120)) throw std::runtime_error("bad header");
  std::vector<Row> rows(nrows);
  for(uint32_t r=0;r<nrows;r++){
    uint8_t a,b; uint16_t pad; uint32_t nnz;
    read_exact(f,(char*)&a,1,"a"); read_exact(f,(char*)&b,1,"b");
    read_exact(f,(char*)&pad,2,"pad"); read_exact(f,(char*)&nnz,4,"nnz");
    if(a>=16 || b>=16 || pad!=0 || nnz>50000000U) throw std::runtime_error("invalid row header");
    rows[r].a=a; rows[r].b=b; rows[r].e.resize(nnz);
    for(uint32_t i=0;i<nnz;i++){
      read_exact(f,(char*)&rows[r].e[i].key,4,"key"); read_exact(f,(char*)&rows[r].e[i].val,4,"value");
      for(int j=0;j<6;j++) if(((rows[r].e[i].key>>(4*j))&15U)>=16U) throw std::runtime_error("encoded value outside range");
    }
  }
  char extra; if(f.read(&extra,1)) throw std::runtime_error("trailing bytes");
  if(!f.eof()) throw std::runtime_error("stream error after payload");
  return rows;
}

static int parity_vec(const std::vector<int>& p){ int inv=0; for(size_t i=0;i<p.size();i++)for(size_t j=i+1;j<p.size();j++)inv += p[i]>p[j]; return inv&1?-1:1; }

static std::vector<std::pair<Perm,int>> subgroup(const std::vector<std::vector<int>>& blocks){
  std::vector<std::pair<Perm,int>> out;
  Perm id{}; for(int i=0;i<6;i++)id[i]=i;
  std::function<void(size_t,Perm,int)> rec = [&](size_t bi,Perm cur,int sgn){
    if(bi==blocks.size()){out.push_back({cur,sgn});return;}
    auto block=blocks[bi]; std::sort(block.begin(),block.end());
    do{
      Perm nxt=cur;
      for(size_t q=0;q<blocks[bi].size();q++) nxt[blocks[bi][q]]=block[q];
      std::vector<int> idx; for(int x:block){auto it=std::find(blocks[bi].begin(),blocks[bi].end(),x); idx.push_back((int)(it-blocks[bi].begin()));}
      rec(bi+1,nxt,sgn*parity_vec(idx));
    }while(std::next_permutation(block.begin(),block.end()));
  };
  rec(0,id,1); return out;
}

static uint32_t encode_perm(const Perm&p){uint32_t x=0;for(int i=0;i<6;i++)x|=((uint32_t)p[i])<<(3*i);return x;}
static Perm compose(const Perm&r,const Perm&c){Perm z{};for(int i=0;i<6;i++)z[i]=c[r[i]];return z;}

struct Tableau { std::vector<std::vector<int>> rows,cols; std::vector<Term> terms; };

static Tableau make_tableau(const std::vector<int>& shape,const std::vector<int>& cells){
  Tableau t; int q=0;
  for(int len:shape){std::vector<int> row;for(int j=0;j<len;j++)row.push_back(cells[q++]);t.rows.push_back(row);}
  for(int j=0;j<*std::max_element(shape.begin(),shape.end());j++){std::vector<int> col;for(size_t i=0;i<t.rows.size();i++)if(j<(int)t.rows[i].size())col.push_back(t.rows[i][j]);t.cols.push_back(col);}
  auto rg=subgroup(t.rows), cg=subgroup(t.cols);
  std::map<uint32_t,std::pair<Perm,int>> mp;
  for(auto &rr:rg) for(auto &cc:cg){ Perm z=compose(rr.first,cc.first); uint32_t e=encode_perm(z); auto it=mp.find(e); if(it==mp.end())mp[e]={z,cc.second}; else it->second.second += cc.second; }
  for(auto &kv:mp) if(kv.second.second) t.terms.push_back({kv.second.first,kv.second.second});
  return t;
}

static std::vector<Tableau> standard_tableaux(const std::vector<int>& shape){
  std::vector<Tableau> out; std::vector<int> cells(6); std::iota(cells.begin(),cells.end(),0);
  do{
    bool ok=true; int q=0; std::vector<std::vector<int>> rows;
    for(int len:shape){std::vector<int> row;for(int j=0;j<len;j++)row.push_back(cells[q++]);rows.push_back(row);}
    for(auto&r:rows)for(size_t j=1;j<r.size();j++)if(r[j-1]>r[j])ok=false;
    for(int j=0;j<*std::max_element(shape.begin(),shape.end());j++){int prev=-1;for(size_t i=0;i<rows.size();i++)if(j<(int)rows[i].size()){if(prev>=0 && prev>rows[i][j])ok=false;prev=rows[i][j];}}
    if(ok)out.push_back(make_tableau(shape,cells));
  }while(std::next_permutation(cells.begin(),cells.end()));
  return out;
}

static uint32_t permute_key(uint32_t key,const Perm&p){
  uint32_t z=0; for(int i=0;i<6;i++){uint32_t v=(key>>(4*p[i]))&15U;z|=v<<(4*i);} return z;
}

static int dense_rank(std::vector<std::vector<int>> A,int p){
  int m=A.size(), n=A.empty()?0:A[0].size(), r=0;
  for(int c=0;c<n && r<m;c++){
    int piv=r; while(piv<m && A[piv][c]==0)piv++; if(piv==m)continue;
    std::swap(A[piv],A[r]); int inv=modpow(A[r][c],p-2,p);
    for(int j=c;j<n;j++)A[r][j]=(int)((long long)A[r][j]*inv%p);
    for(int i=0;i<m;i++)if(i!=r && A[i][c]){int f=A[i][c];for(int j=c;j<n;j++)A[i][j]=modnorm(A[i][j]-(long long)f*A[r][j],p);} r++;
  }return r;
}

static int sketched_rank(const std::vector<Row>&rows,const std::vector<Term>&terms,int p,int B,uint64_t seed){
  std::vector<std::vector<int>> A(rows.size(),std::vector<int>(B));
  #pragma omp parallel for schedule(dynamic,1)
  for(int ri=0;ri<(int)rows.size();ri++){
    auto &dst=A[ri];
    for(const auto &en:rows[ri].e){
      for(const auto &tm:terms){
        uint32_t nk=permute_key(en.key,tm.p); uint64_t h=splitmix64(((uint64_t)nk<<1)^seed);
        int b=(int)(h%B); int s=(h>>63)?1:-1;
        long long add=(long long)en.val*tm.coeff*s;
        dst[b]=modnorm(dst[b]+add,p);
      }
    }
  }
  return dense_rank(std::move(A),p);
}

static std::string vecjson(const std::vector<int>&v){std::ostringstream o;o<<"[";for(size_t i=0;i<v.size();i++){if(i)o<<",";o<<v[i];}o<<"]";return o.str();}
static std::string rowsjson(const Tableau&t){std::ostringstream o;o<<"[";for(size_t i=0;i<t.rows.size();i++){if(i)o<<",";o<<vecjson(t.rows[i]);}o<<"]";return o.str();}

int main(int argc,char**argv){
  std::string input,shape_s="4,2"; int p=1009,B=192,seeds=2; bool scan=true; int chosen=-1;
  for(int i=1;i<argc;i++){std::string a=argv[i]; if(a=="--input")input=argv[++i]; else if(a=="--shape")shape_s=argv[++i]; else if(a=="--prime")p=std::stoi(argv[++i]); else if(a=="--buckets")B=std::stoi(argv[++i]); else if(a=="--seeds")seeds=std::stoi(argv[++i]); else if(a=="--index"){chosen=std::stoi(argv[++i]);scan=false;} }
  if(input.empty()){std::cerr<<"--input required\n";return 2;}
  std::vector<int> shape; std::stringstream ss(shape_s);std::string tok;while(std::getline(ss,tok,','))shape.push_back(std::stoi(tok));
  auto rows=read_rows(input); auto tabs=standard_tableaux(shape);
  std::vector<int> indices; if(scan){for(int i=0;i<(int)tabs.size();i++)indices.push_back(i);}else indices.push_back(chosen);
  std::cout<<"{\"shape\":"<<vecjson(shape)<<",\"tableau_count\":"<<tabs.size()<<",\"results\":[";
  bool first=true;
  for(int idx:indices){ if(idx<0||idx>=(int)tabs.size())throw std::runtime_error("bad index"); auto&t=tabs[idx]; std::vector<int> ranks;
    for(int s=0;s<seeds;s++)ranks.push_back(sketched_rank(rows,t.terms,p,B,0x123456789abcdef0ULL+0x9e3779b97f4a7c15ULL*s));
    if(!first)std::cout<<",";first=false;
    std::cout<<"{\"index\":"<<idx<<",\"rows\":"<<rowsjson(t)<<",\"terms\":"<<t.terms.size()<<",\"ranks\":"<<vecjson(ranks)<<"}"<<std::flush;
  }
  std::cout<<"]}\n";
}
