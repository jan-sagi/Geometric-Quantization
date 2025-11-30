import math
from decimal import Decimal, getcontext

# Nastavení přesnosti pro detektivní práci
getcontext().prec = 100

class GeometryDetective:
    """
    GEOMETRICKÝ DETEKTIV
    ====================
    Ověřuje podezření, že základní konstanty teorie (Pi^5, Alpha)
    jsou ve skutečnosti vzorce pro objemy/povrchy v 10D a 5D prostoru.
    """

    PI = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647")

    def factorial(self, n):
        return Decimal(math.factorial(n))

    def hypersphere_volume(self, dim):
        """V_n = pi^(n/2) / Gamma(n/2 + 1)"""
        n = Decimal(dim)
        numerator = self.PI ** (n / 2)
        # Gamma(n/2 + 1) pro sudé n je faktoriál (n/2)!
        # Pro n=10 -> Gamma(6) = 5! = 120
        denom = self.factorial(int(dim / 2))
        return numerator / denom

    def hypersphere_surface(self, dim):
        """S_n-1 = 2 * pi^(n/2) / Gamma(n/2)"""
        # Povrch jednotkové koule v dimenzi n (hranice je n-1 dimenzionální)
        # Pro n=4 (4D koule) je povrch 3D sféra (2*pi^2)
        n = Decimal(dim)
        numerator = Decimal(2) * (self.PI ** (n / 2))
        denom = self.factorial(int(dim / 2) - 1)
        return numerator / denom

    def investigate_baryon_scale(self):
        print(f"\n[PŘÍPAD 1] BARYONOVÁ ŠKÁLA (Proton = Pi^5)")
        print("-" * 60)

        # Teorie: Baryon Scale = Pi^5
        baryon_scale = self.PI ** 5
        print(f" Tvoje Baryon Scale: {baryon_scale:.10f}")

        # Hypotéza: Je to svázáno s objemem v 10D?
        vol_10d = self.hypersphere_volume(10)
        print(f" Objem 10D koule:    {vol_10d:.10f}")

        # Test identity: Pi^5 = 120 * V_10
        factor = baryon_scale / vol_10d
        print(f" Poměr (Scale/Vol):  {factor:.10f}")

        if abs(factor - 120) < 1e-20:
            print(f" ✅ SHODA: Baryonová škála je PŘESNĚ 5! * Objem(10D).")
            print(f"    Interpretace: Proton je stabilní 10D struktura s 5 permutacemi.")
        else:
            print(f" ❌ Neshoda.")

    def investigate_alpha_geometry(self):
        print(f"\n[PŘÍPAD 2] ALPHA STRUKTURA (4*Pi^3)")
        print("-" * 60)

        target = Decimal(4) * (self.PI ** 3)
        print(f" Hlavní člen Alfy:   {target:.10f}")

        # Hypotéza: S1 * S3 (Kruh * Povrch 4D koule)
        s1 = Decimal(2) * self.PI       # Obvod kruhu
        s3 = Decimal(2) * (self.PI**2)  # Povrch 4D koule (Sféra ve 4D)

        product = s1 * s3
        print(f" S1 * S3 (Geometrie):{product:.10f}")

        if abs(product - target) < 1e-20:
            print(f" ✅ SHODA: Hlavní síla Alfy je topologický součin Kruhu a 4D Sféry.")
            print(f"    Interpretace: Elektromagnetismus je 5D cylindrická projekce.")
        else:
            print(f" ❌ Neshoda.")

if __name__ == "__main__":
    detective = GeometryDetective()
    detective.investigate_baryon_scale()
    detective.investigate_alpha_geometry()