<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class LeastSquaresController extends AbstractController
{
    #[Route('/least-squares', name: 'app_least_squares')]
    public function index(Request $request): Response
    {
        $pointsX   = [];
        $pointsY   = [];
        $degree    = 1;
        $result    = null;
        $polynomial = null;
        $chartData = null;
        $error     = null;

        if ($request->isMethod('POST')) {
            $pointsX = $request->request->all('x') ?: [];
            $pointsY = $request->request->all('y') ?: [];
            $degree  = (int) $request->request->get('degree', 1);

            try {
                $n = count($pointsX);
                if ($n < $degree + 1) {
                    throw new \Exception('Il faut au moins ' . ($degree + 1) . ' points pour un polynôme de degré ' . $degree . '.');
                }

                $x = array_map('floatval', $pointsX);
                $y = array_map('floatval', $pointsY);

                // Matrice de Vandermonde A (n x (degree+1))
                $A = [];
                for ($i = 0; $i < $n; $i++) {
                    for ($j = 0; $j <= $degree; $j++) {
                        $A[$i][$j] = pow($x[$i], $j);
                    }
                }

                // tA * A  (taille (degree+1) x (degree+1))
                $AtA = [];
                for ($i = 0; $i <= $degree; $i++) {
                    for ($j = 0; $j <= $degree; $j++) {
                        $s = 0.0;
                        for ($k = 0; $k < $n; $k++) $s += $A[$k][$i] * $A[$k][$j];
                        $AtA[$i][$j] = $s;
                    }
                }

                // tA * Y  (taille degree+1)
                $AtY = [];
                for ($i = 0; $i <= $degree; $i++) {
                    $s = 0.0;
                    for ($k = 0; $k < $n; $k++) $s += $A[$k][$i] * $y[$k];
                    $AtY[$i] = $s;
                }

                // Résolution par élimination de Gauss avec pivot partiel
                $coeffs = $this->gaussSolve($AtA, $AtY, $degree + 1);

                $result = array_map([$this, 'formatNum'], $coeffs);
                $polynomial = $this->buildPolynomial($coeffs);
                $chartData  = $this->prepareChart($x, $y, $coeffs);

            } catch (\Exception $e) {
                $error = $e->getMessage();
            }
        }

        return $this->render('least_squares/index.html.twig', [
            'pointsX'    => $pointsX,
            'pointsY'    => $pointsY,
            'degree'     => $degree,
            'result'     => $result,
            'polynomial' => $polynomial,
            'chartData'  => $chartData,
            'error'      => $error,
        ]);
    }

    // Élimination de Gauss avec pivot partiel
    private function gaussSolve(array $M, array $b, int $n): array
    {
        // Augmented matrix
        for ($i = 0; $i < $n; $i++) $M[$i][$n] = $b[$i];

        for ($col = 0; $col < $n; $col++) {
            // Pivot partiel
            $maxRow = $col;
            for ($row = $col + 1; $row < $n; $row++) {
                if (abs($M[$row][$col]) > abs($M[$maxRow][$col])) $maxRow = $row;
            }
            [$M[$col], $M[$maxRow]] = [$M[$maxRow], $M[$col]];

            if (abs($M[$col][$col]) < 1e-12) throw new \Exception('Système singulier — vérifiez vos points.');

            for ($row = $col + 1; $row < $n; $row++) {
                $f = $M[$row][$col] / $M[$col][$col];
                for ($k = $col; $k <= $n; $k++) $M[$row][$k] -= $f * $M[$col][$k];
            }
        }

        // Substitution arrière
        $x = array_fill(0, $n, 0.0);
        for ($i = $n - 1; $i >= 0; $i--) {
            $x[$i] = $M[$i][$n];
            for ($j = $i + 1; $j < $n; $j++) $x[$i] -= $M[$i][$j] * $x[$j];
            $x[$i] /= $M[$i][$i];
        }
        return $x;
    }

    private function buildPolynomial(array $coeffs): string
    {
        $terms = [];
        for ($i = count($coeffs) - 1; $i >= 0; $i--) {
            $c = $coeffs[$i];
            if (abs($c) < 1e-10) continue;
            $cStr = $this->formatNum(abs($c));
            $sign = $c >= 0 ? '+' : '-';
            if ($i === 0)      $term = $cStr;
            elseif ($i === 1)  $term = ($cStr === '1' ? '' : $cStr) . 'x';
            else               $term = ($cStr === '1' ? '' : $cStr) . "x<sup>$i</sup>";
            $terms[] = ['sign' => $sign, 'term' => $term];
        }
        if (empty($terms)) return '0';
        $str = ($terms[0]['sign'] === '-' ? '-' : '') . $terms[0]['term'];
        for ($i = 1; $i < count($terms); $i++) $str .= ' ' . $terms[$i]['sign'] . ' ' . $terms[$i]['term'];
        return $str;
    }

    private function prepareChart(array $x, array $y, array $coeffs): array
    {
        $minX = min($x); $maxX = max($x);
        $range = max($maxX - $minX, 1);
        $extMin = $minX - $range * 0.3;
        $extMax = $maxX + $range * 0.3;

        $chartX = []; $chartY = [];
        for ($i = 0; $i <= 200; $i++) {
            $xi = $extMin + ($extMax - $extMin) * ($i / 200);
            $yi = 0.0;
            foreach ($coeffs as $j => $c) $yi += $c * pow($xi, $j);
            $chartX[] = round($xi, 4);
            $chartY[] = round($yi, 6);
        }

        $points = [];
        for ($i = 0; $i < count($x); $i++) $points[] = ['x' => $x[$i], 'y' => $y[$i]];

        return ['labels' => $chartX, 'data' => $chartY, 'points' => $points];
    }

    private function formatNum(float $v): string
    {
        if (abs($v - round($v)) < 1e-9) return (string)(int)round($v);
        return rtrim(rtrim(number_format($v, 6, '.', ''), '0'), '.');
    }
}
